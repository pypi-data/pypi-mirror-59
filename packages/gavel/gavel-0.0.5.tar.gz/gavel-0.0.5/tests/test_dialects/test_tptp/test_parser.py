from gavel.dialects.tptp.parser import TPTPParser, TPTPProblemParser, SimpleTPTPProofParser
from gavel.dialects.tptp.compiler import TPTPCompiler
from gavel.logic import logic
from gavel.logic import problem
from gavel.logic import proof
from ..test_base.test_parser import TestLogicParser, check_wrapper, TestProblemParser, TestProofParser
from gavel.config.settings import TPTP_ROOT
import os
import unittest
import multiprocessing as mp
from unittest import skip


class TestTPTPParser(TestLogicParser):
    _parser_cls = TPTPParser

    def test_verum(self):
        inp = """fof(mElmSort,axiom,(
    ! [W0] :
      ( aElement0(W0)
     => $true ) ))."""
        result = problem.AnnotatedFormula(
            logic="fof",
            name="mElmSort",
            role=problem.FormulaRole.AXIOM,
            formula=logic.QuantifiedFormula(
                quantifier=logic.Quantifier.UNIVERSAL,
                variables=[logic.Variable("W0")],
                formula=logic.BinaryFormula(
                    left=logic.PredicateExpression(
                        predicate="aElement0", arguments=[logic.Variable("W0")]
                    ),
                    operator=logic.BinaryConnective.IMPLICATION,
                    right=logic.DefinedConstant.VERUM,
                ),
            ),
        )
        self.check_parser(inp, result)

    def test_functor(self):
        inp = """cnf(and_definition1,axiom,( and(X,n0) = n0 ))."""
        result = problem.AnnotatedFormula(
            logic="cnf",
            name="and_definition1",
            role=problem.FormulaRole.AXIOM,
            formula=logic.BinaryFormula(
                left=logic.FunctorExpression(
                    functor="and", arguments=[logic.Variable("X"), logic.Constant("n0")]
                ),
                operator=logic.BinaryConnective.EQ,
                right=logic.Constant("n0"),
            ),
        )
        self.check_parser(inp, result)

    @check_wrapper()
    def test_single_quote(self):
        inp = "p('This is arbitrary text')"
        result = logic.PredicateExpression(
            "p", [logic.Constant("'This is arbitrary text'")]
        )
        return inp, result

    @check_wrapper()
    def test_double_quote(self):
        inp = 'p("This is arbitrary text")'
        result = logic.PredicateExpression(
            "p", [logic.DistinctObject('"This is arbitrary text"')]
        )
        return inp, result

    @check_wrapper()
    def test_quantifier(self):
        inp = "![X1,X2]:?[Y1,Y2]:p(X1,X2,Y1,Y2)"
        result = logic.QuantifiedFormula(
            logic.Quantifier.UNIVERSAL,
            [logic.Variable("X1"), logic.Variable("X2")],
            logic.QuantifiedFormula(
                logic.Quantifier.EXISTENTIAL,
                [logic.Variable("Y1"), logic.Variable("Y2")],
                logic.PredicateExpression(
                    "p",
                    [
                        logic.Variable("X1"),
                        logic.Variable("X2"),
                        logic.Variable("Y1"),
                        logic.Variable("Y2"),
                    ],
                ),
            ),
        )
        return inp, result


class TestTPTPProblemParser(TestProblemParser):
    _parser_cls = TPTPProblemParser

    def test_problems_1(self):
        inp = """fof(a1, axiom, p(a) => q(a)).
fof(a2, axiom, q(a) => $false).
fof(a3, axiom, $true => p(a)).
fof(c, conjecture, $false)."""
        result = [
            problem.Problem(
                premises=[
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a1",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("a")]
                            ),
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.PredicateExpression(
                                predicate="q", arguments=[logic.Constant("a")]
                            ),
                        ),
                    ),
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a2",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.PredicateExpression(
                                predicate="q", arguments=[logic.Constant("a")]
                            ),
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.DefinedConstant.FALSUM,
                        ),
                    ),
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a3",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.DefinedConstant.VERUM,
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("a")]
                            ),
                        ),
                    ),
                ],
                conjecture=problem.AnnotatedFormula(
                    logic="fof",
                    name="c",
                    role=problem.FormulaRole.CONJECTURE,
                    formula=logic.DefinedConstant.FALSUM,
                ),
            )
        ]

        self.check_parser(inp, result)

    def test_problems_2(self):
        inp = """fof(a1, axiom, (p(a) & p(b) & p(d)) => $false).
fof(a2, axiom, p(e)  => $false).
fof(a3, axiom, p(c) => p(a)).
fof(a4, axiom, p(c)   => $false).
fof(a5, axiom, p(a) => p(d)).
fof(c, conjecture, $false)."""
        result = [
            problem.Problem(
                premises=[
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a1",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.BinaryFormula(
                                left=logic.PredicateExpression(
                                    predicate="p", arguments=[logic.Constant("a")]
                                ),
                                operator=logic.BinaryConnective.CONJUNCTION,
                                right=logic.BinaryFormula(
                                    left=logic.PredicateExpression(
                                        predicate="p", arguments=[logic.Constant("b")]
                                    ),
                                    operator=logic.BinaryConnective.CONJUNCTION,
                                    right=logic.PredicateExpression(
                                        predicate="p", arguments=[logic.Constant("d")]
                                    ),
                                ),
                            ),
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.DefinedConstant.FALSUM,
                        ),
                    ),
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a2",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("e")]
                            ),
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.DefinedConstant.FALSUM,
                        ),
                    ),
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a3",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("c")]
                            ),
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("a")]
                            ),
                        ),
                    ),
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a4",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("c")]
                            ),
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.DefinedConstant.FALSUM,
                        ),
                    ),
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a5",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("a")]
                            ),
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("d")]
                            ),
                        ),
                    ),
                ],
                conjecture=problem.AnnotatedFormula(
                    logic="fof",
                    name="c",
                    role=problem.FormulaRole.CONJECTURE,
                    formula=logic.DefinedConstant.FALSUM,
                ),
            )
        ]
        self.check_parser(inp, result)

    def test_problems_3(self):
        inp = """fof(a1, axiom, (p(e) & p(b) & p(d)) => $false).
fof(a2, axiom, p(e) => p(d)).
fof(a3, axiom, $true => p(f)).
fof(a4, axiom, p(a) => $false).
fof(a5, axiom, p(c) => p(e)).
fof(a6, axiom, $true => p(c)).
fof(c, conjecture, $false)."""
        result = [
            problem.Problem(
                premises=[
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a1",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.BinaryFormula(
                                left=logic.PredicateExpression(
                                    predicate="p", arguments=[logic.Constant("e")]
                                ),
                                operator=logic.BinaryConnective.CONJUNCTION,
                                right=logic.BinaryFormula(
                                    left=logic.PredicateExpression(
                                        predicate="p", arguments=[logic.Constant("b")]
                                    ),
                                    operator=logic.BinaryConnective.CONJUNCTION,
                                    right=logic.PredicateExpression(
                                        predicate="p", arguments=[logic.Constant("d")]
                                    ),
                                ),
                            ),
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.DefinedConstant.FALSUM,
                        ),
                    ),
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a2",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("e")]
                            ),
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("d")]
                            ),
                        ),
                    ),
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a3",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.DefinedConstant.VERUM,
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("f")]
                            ),
                        ),
                    ),
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a4",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("a")]
                            ),
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.DefinedConstant.FALSUM,
                        ),
                    ),
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a5",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("c")]
                            ),
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("e")]
                            ),
                        ),
                    ),
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a6",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.DefinedConstant.VERUM,
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("c")]
                            ),
                        ),
                    ),
                ],
                conjecture=problem.AnnotatedFormula(
                    logic="fof",
                    name="c",
                    role=problem.FormulaRole.CONJECTURE,
                    formula=logic.DefinedConstant.FALSUM,
                ),
            )
        ]
        self.check_parser(inp, result)


    def test_problems_4(self):
        inp = """fof(a1, axiom, (p(e) & p(b) & p(d)) => $false).
fof(a2, axiom, p(e) => p(d)).
fof(a3, axiom, $true => p(b)).
fof(a4, axiom, p(a) => $false).
fof(a5, axiom, p(c) => p(e)).
fof(a6, axiom, $true => p(c)).
fof(c, conjecture, $false)."""
        result = [
            problem.Problem(
                premises=[
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a1",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.BinaryFormula(
                                left=logic.PredicateExpression(
                                    predicate="p", arguments=[logic.Constant("e")]
                                ),
                                operator=logic.BinaryConnective.CONJUNCTION,
                                right=logic.BinaryFormula(
                                    left=logic.PredicateExpression(
                                        predicate="p", arguments=[logic.Constant("b")]
                                    ),
                                    operator=logic.BinaryConnective.CONJUNCTION,
                                    right=logic.PredicateExpression(
                                        predicate="p", arguments=[logic.Constant("d")]
                                    ),
                                ),
                            ),
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.DefinedConstant.FALSUM,
                        ),
                    ),
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a2",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("e")]
                            ),
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("d")]
                            ),
                        ),
                    ),
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a3",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.DefinedConstant.VERUM,
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("b")]
                            ),
                        ),
                    ),
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a4",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("a")]
                            ),
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.DefinedConstant.FALSUM,
                        ),
                    ),
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a5",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("c")]
                            ),
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("e")]
                            ),
                        ),
                    ),
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a6",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.DefinedConstant.VERUM,
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("c")]
                            ),
                        ),
                    ),
                ],
                conjecture=problem.AnnotatedFormula(
                    logic="fof",
                    name="c",
                    role=problem.FormulaRole.CONJECTURE,
                    formula=logic.DefinedConstant.FALSUM,
                ),
            )
        ]
        self.check_parser(inp, result)

    def test_problems_2_1(self):
        inp = """fof(a1, axiom, (p(e) & p(b) & p(d)) => $false).
fof(a2, axiom, p(e) => p(d)).
fof(a3, axiom, $true => p(f)).
fof(a4, axiom, p(a) => $false).
fof(a5, axiom, p(c) => p(e)).
fof(a6, axiom, $true => p(c)).
fof(a7, axiom, $true => (f=b)).
fof(c, conjecture, $false)."""
        result = [
            problem.Problem(
                premises=[
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a1",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.BinaryFormula(
                                left=logic.PredicateExpression(
                                    predicate="p", arguments=[logic.Constant("e")]
                                ),
                                operator=logic.BinaryConnective.CONJUNCTION,
                                right=logic.BinaryFormula(
                                    left=logic.PredicateExpression(
                                        predicate="p", arguments=[logic.Constant("b")]
                                    ),
                                    operator=logic.BinaryConnective.CONJUNCTION,
                                    right=logic.PredicateExpression(
                                        predicate="p", arguments=[logic.Constant("d")]
                                    ),
                                ),
                            ),
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.DefinedConstant.FALSUM,
                        ),
                    ),
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a2",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("e")]
                            ),
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("d")]
                            ),
                        ),
                    ),
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a3",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.DefinedConstant.VERUM,
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("f")]
                            ),
                        ),
                    ),
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a4",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("a")]
                            ),
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.DefinedConstant.FALSUM,
                        ),
                    ),
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a5",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("c")]
                            ),
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("e")]
                            ),
                        ),
                    ),
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a6",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.DefinedConstant.VERUM,
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("c")]
                            ),
                        ),
                    ),
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a7",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.DefinedConstant.VERUM,
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.BinaryFormula(
                                left=logic.Constant("f"),
                                operator=logic.BinaryConnective.EQ,
                                right=logic.Constant("b")
                            ),
                        ),
                    ),
                ],
                conjecture=problem.AnnotatedFormula(
                    logic="fof",
                    name="c",
                    role=problem.FormulaRole.CONJECTURE,
                    formula=logic.DefinedConstant.FALSUM,
                ),
            )
        ]
        self.check_parser(inp, result)

    def test_problems_2_2(self):
        inp = """fof(a1, axiom, $true => a=d).
fof(a2, axiom, $true => p(g(f(a),b))).
fof(a3, axiom, $true => f(d)=b).
fof(a4, axiom, $true => g(b,b)=c).
fof(a5, axiom, p(c) => $false).
fof(c, conjecture, $false)."""
        result = [
            problem.Problem(
                premises=[
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a1",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.DefinedConstant.VERUM,
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.BinaryFormula(
                                left=logic.Constant("a"),
                                operator=logic.BinaryConnective.EQ,
                                right=logic.Constant("d")
                            ),
                        ),
                    ),
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a2",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.DefinedConstant.VERUM,
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.PredicateExpression(
                                predicate="p",
                                arguments=[logic.FunctorExpression(
                                    functor="g",
                                    arguments=[logic.FunctorExpression(
                                        functor="f",
                                        arguments=[logic.Constant("a")]
                                    ),logic.Constant("b")]
                                ),]
                            ),
                        ),
                    ),
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a3",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.DefinedConstant.VERUM,
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.BinaryFormula(
                                left=logic.FunctorExpression(
                                    functor="f",
                                    arguments=[logic.Constant("d")]
                                ),
                                operator=logic.BinaryConnective.EQ,
                                right=logic.Constant("b")
                            ),
                        ),
                    ),
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a4",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.DefinedConstant.VERUM,
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.BinaryFormula(
                                left=logic.FunctorExpression(
                                    functor="g",
                                    arguments=[logic.Constant("b"), logic.Constant("b")]
                                ),
                                operator=logic.BinaryConnective.EQ,
                                right=logic.Constant("c")
                            ),
                        ),
                    ),
                    problem.AnnotatedFormula(
                        logic="fof",
                        name="a5",
                        role=problem.FormulaRole.AXIOM,
                        formula=logic.BinaryFormula(
                            left=logic.PredicateExpression(
                                predicate="p", arguments=[logic.Constant("c")]
                            ),
                            operator=logic.BinaryConnective.IMPLICATION,
                            right=logic.DefinedConstant.FALSUM,
                        ),
                    ),
                ],
                conjecture=problem.AnnotatedFormula(
                    logic="fof",
                    name="c",
                    role=problem.FormulaRole.CONJECTURE,
                    formula=logic.DefinedConstant.FALSUM,
                ),
            )
        ]
        self.check_parser(inp, result)


class TestTPTPProofParser(TestProofParser):
    _parser_cls = SimpleTPTPProofParser
    def test_proof(self):
        inp = """
        cnf(a1, axiom,
            $false,
            file('/tmp/./_prove_a_equals_aUa405201937553918865.tptp',
                 member_of_set2_is_member_of_union)).
        cnf(a2, axiom,
            $false,
            file('/tmp/./_prove_a_equals_aUa405201937553918865.tptp',
                 a_union_a_is_aUa)).
        cnf(a3, axiom,
            $false,
            file('/tmp/./_prove_a_equals_aUa405201937553918865.tptp',
                 subsets_axiom2)).
        cnf(a4, axiom, $false,
            file('/tmp/./_prove_a_equals_aUa405201937553918865.tptp',
                 member_of_union_is_member_of_one_set)).
        cnf(nc1, negated_conjecture, $false,
            file('/tmp/./_prove_a_equals_aUa405201937553918865.tptp',
                 prove_a_equals_aUa)).
        cnf(a5, axiom, $false,
            file('/tmp/./_prove_a_equals_aUa405201937553918865.tptp',
                 subsets_are_set_equal_sets)).
        cnf(a6, axiom,$false,
            file('/tmp/./_prove_a_equals_aUa405201937553918865.tptp',
                 subsets_axiom1)).
        cnf(a7, axiom, $false,
            member_of_set2_is_member_of_union).
        cnf(h1, hypothesis, $false, a_union_a_is_aUa).
        cnf(a8, axiom,
            $false,
            subsets_axiom2).
        cnf(h2, hypothesis, $false,
            inference(spm, [status(thm)], [c_0_7, c_0_8])).
        cnf(a9, axiom, $false,
            member_of_union_is_member_of_one_set).
        cnf(nc2, negated_conjecture, $false, prove_a_equals_aUa).
        cnf(a10, axiom, $false,
            subsets_are_set_equal_sets).
        cnf(h3, hypothesis,
            $false,
            inference(spm, [status(thm)], [c_0_9, c_0_10])).
        cnf(a11, axiom,
            $false,
            subsets_axiom1).
        cnf(h4, hypothesis, $false,
            inference(spm, [status(thm)], [c_0_11, c_0_8])).
        cnf(nc3, negated_conjecture, $false,
            inference(spm, [status(thm)], [c_0_12, c_0_13])).
        cnf(h5, hypothesis, $false,
            inference(spm, [status(thm)], [c_0_14, c_0_15])).
        cnf(h6, hypothesis,
            $false,
            inference(spm, [status(thm)], [c_0_16, c_0_15])).
        cnf(nc4, negated_conjecture, $false,
            inference(cn, [status(thm)],
                      [inference(rw, [status(thm)], [c_0_17, c_0_18])])).
        cnf(h7, hypothesis, ($false), inference(sr, [status(thm)], [
            inference(spm, [status(thm)], [c_0_9, c_0_19]), c_0_20]), ['proof'])."""
        result = proof.LinearProof(steps=[
            proof.Axiom(name="a1", formula=logic.DefinedConstant.FALSUM),
            proof.Axiom(name="a2", formula=logic.DefinedConstant.FALSUM),
            proof.Axiom(name="a3", formula=logic.DefinedConstant.FALSUM),
            proof.Axiom(name="a4", formula=logic.DefinedConstant.FALSUM),
            proof.Axiom(name="nc1", formula=logic.DefinedConstant.FALSUM),
            proof.Axiom(name="a5", formula=logic.DefinedConstant.FALSUM),
            proof.Axiom(name="a6", formula=logic.DefinedConstant.FALSUM),
            proof.Axiom(name="a7", formula=logic.DefinedConstant.FALSUM),
            proof.Axiom(name="h1", formula=logic.DefinedConstant.FALSUM),
            proof.Axiom(name="a8", formula=logic.DefinedConstant.FALSUM),
            proof.Axiom(name="h2", formula=logic.DefinedConstant.FALSUM),
            proof.Axiom(name="a9", formula=logic.DefinedConstant.FALSUM),
            proof.Axiom(name="nc2", formula=logic.DefinedConstant.FALSUM),
            proof.Axiom(name="a10", formula=logic.DefinedConstant.FALSUM),
            proof.Axiom(name="h3", formula=logic.DefinedConstant.FALSUM),
            proof.Axiom(name="a11", formula=logic.DefinedConstant.FALSUM),
            proof.Axiom(name="h4", formula=logic.DefinedConstant.FALSUM),
            proof.Axiom(name="nc3", formula=logic.DefinedConstant.FALSUM),
            proof.Axiom(name="h5", formula=logic.DefinedConstant.FALSUM),
            proof.Axiom(name="h6", formula=logic.DefinedConstant.FALSUM),
            proof.Axiom(name="nc4", formula=logic.DefinedConstant.FALSUM),
            proof.Axiom(name="h7", formula=logic.DefinedConstant.FALSUM),
        ])
        self.check_parser(inp, result)

"""
class TestTHFParser(TestLogicParser):
    _parser_cls = TPTPParser

    @skip
    def test_type_formula(self):
        inp = "thf(prop_a,type,(
    prop_a: $i > $o ))."
        expected = problem.AnnotatedFormula(
            logic="thf",
            name="prop_a",
            role=problem.FormulaRole.TYPE,
            formula=logic.TypeFormula(
                name=logic.Constant("prop_a"),
                type_expression=logic.MappingType(
                    left="$i",
                    right="$o"
                )
            )
        )
        self.check_parser(inp, expected)
"""
