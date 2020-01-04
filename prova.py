import wmipa

import mathsat
from pysmt.shortcuts import *
from pysmt.typing import REAL
from math import fsum

from wmipa import logger
from wmipa.utils import get_boolean_variables

newSolver = True

class MyWMI(wmipa.WMI):

    def _compute_TTAs(self, formula):

        # Label LRA atoms with fresh boolean variables
        labelled_formula, pa_vars, labels = self.label_formula(formula, formula.get_atoms())

        # Perform AllSMT on the labelled formula

        if newSolver:
            solver = Solver(name="msat", solver_options={"dpll.allsat_minimize_model": "true", "dpll.allsat_allow_duplicates": "false", "preprocessor.toplevel_propagation": "false", "preprocessor.simplification": "0"})
        else:
            solver = Solver(name="msat")

        converter = solver.converter
        solver.add_assertion(labelled_formula)
        models = []
        mathsat.msat_all_sat(solver.msat_env(),
                             [converter.convert(v) for v in pa_vars],
                             lambda model: wmipa.WMI._callback(model, converter, models))
        return models, labels


    def _compute_WMI_AllSMT(self, formula, weights):
        models, labels = self._compute_TTAs(formula)
        problems = []
        for index, model in enumerate(models):
            # retrieve truth assignments for the original atoms of the formula
            atom_assignments = {}
            for atom, value in wmipa.WMI._get_assignments(model).items():
                if atom in labels:
                    atom = labels[atom]
                atom_assignments[atom] = value
            problem = self._create_problem(atom_assignments, weights)
            problems.append(problem)

        volume = fsum(self.integrator.integrate_batch(problems))
        return volume, len(problems)

    def _compute_WMI_PA(self, formula, weights):

        problems = []
        boolean_variables = get_boolean_variables(formula)
        if len(boolean_variables) == 0:
            # Enumerate partial TA over theory atoms
            lab_formula, pa_vars, labels = self.label_formula(formula, formula.get_atoms())
            # Predicate abstraction on LRA atoms with minimal models
            for assignments in self._compute_WMI_PA_no_boolean(lab_formula, pa_vars, labels):
                problem = self._create_problem(assignments, weights)
                problems.append(problem)
        else:

            if newSolver:
                solver = Solver(name="msat", solver_options={"dpll.allsat_minimize_model": "true",
                                                             "dpll.allsat_allow_duplicates": "false",
                                                             "preprocessor.toplevel_propagation": "false",
                                                             "preprocessor.simplification": "0"})
            else:
                solver = Solver(name="msat")

            converter = solver.converter
            solver.add_assertion(formula)
            boolean_models = []
            # perform AllSAT on the Boolean variables
            mathsat.msat_all_sat(
                solver.msat_env(),
                [converter.convert(v) for v in boolean_variables],
                lambda model: wmipa.WMI._callback(model, converter, boolean_models))

            logger.debug("n_boolean_models: {}".format(len(boolean_models)))
            # for each boolean assignment mu^A of F
            for model in boolean_models:
                atom_assignments = {}
                boolean_assignments = wmipa.WMI._get_assignments(model)
                atom_assignments.update(boolean_assignments)
                subs = {k: Bool(v) for k, v in boolean_assignments.items()}
                f_next = formula
                # iteratively simplify F[A<-mu^A], getting (possibily part.) mu^LRA
                while True:
                    f_before = f_next
                    f_next = simplify(substitute(f_before, subs))
                    lra_assignments, over = wmipa.WMI._parse_lra_formula(f_next)
                    subs = {k: Bool(v) for k, v in lra_assignments.items()}
                    atom_assignments.update(lra_assignments)
                    if over or lra_assignments == {}:
                        break
                if not over:
                    # predicate abstraction on LRA atoms with minimal models
                    lab_formula, pa_vars, labels = self.label_formula(f_next, f_next.get_atoms())
                    expressions = []
                    for k, v in atom_assignments.items():
                        if k.is_theory_relation():
                            if v:
                                expressions.append(k)
                            else:
                                expressions.append(Not(k))

                    lab_formula = And([lab_formula] + expressions)
                    for assignments in self._compute_WMI_PA_no_boolean(lab_formula, pa_vars, labels, atom_assignments):
                        problem = self._create_problem(assignments, weights)
                        problems.append(problem)
                else:
                    # integrate over mu^A & mu^LRA
                    problem = self._create_problem(atom_assignments, weights)
                    problems.append(problem)

        temp = self.integrator.integrate_batch(problems)
        volume = fsum(temp)
        return volume, len(problems)


# ================================================================================
#                                     Example 1
# ================================================================================
'''
# variables definition
a = Symbol("A", BOOL)
x = Symbol("x", REAL)

# formula definition
phi = And(Iff(a, GE(x, Real(0))),
          GE(x, Real(-1)),
          LE(x, Real(1)))

print("Formula:", serialize(phi))

# weight function definition
w = Ite(GE(x, Real(0)),
        x,
        Times(Real(-1), x))

chi = Bool(True)

print("Weight function:", serialize(w))
print("Support:", serialize(chi))

wmi = MyWMI(chi, w)

print()
for mode in [wmipa.WMI.MODE_ALLSMT, wmipa.WMI.MODE_PA]:
    result, n_integrations = wmi.computeWMI(phi, mode=mode)
    print("WMI with mode {} \t result = {}, \t # integrations = {}".format(mode, result, n_integrations))
'''
# ================================================================================


# ================================================================================
#                                     Example 2
# ================================================================================
'''
# variables definition
a = Symbol("A", BOOL)
x1 = Symbol("x1", REAL)
x2 = Symbol("x2", REAL)

# formula definition
phi = Bool(True)

print("Formula:", serialize(phi))

# weight function definition
w = Plus(Ite(GE(x1, Real(0)),
             Pow(x1, Real(3)),
             Times(Real(-2), x1)),
         Ite(a,
             Times(Real(3), x2),
             Times(Real(-1), Pow(x2, Real(5)))))

chi = And(LE(Real(-1), x1), LT(x1, Real(1)),
          LE(Real(-1), x2), LT(x2, Real(1)),
          Iff(a, GE(x2, Real(0))))

print("Weight function:", serialize(w))
print("Support:", serialize(chi))

wmi = MyWMI(chi, w)
print()
for mode in [wmipa.WMI.MODE_ALLSMT, wmipa.WMI.MODE_PA]:
    result, n_integrations = wmi.computeWMI(phi, mode=mode)
    print("WMI with mode {} \t result = {}, \t # integrations = {}".format(mode, result, n_integrations))
'''
# ================================================================================


# ================================================================================
#                                     Example 3
# ================================================================================
'''
x = Symbol("x", REAL)
y = Symbol("y", REAL)

# formula definition
phi = And(Implies(LE(y, Real(1)), And(LE(Real(0), x), LE(x, Real(2)))),
          Implies(Not(LE(y, Real(1))), And(LE(Real(1), x), LE(x, Real(3)))),
          LE(Real(0), y), LE(y, Real(2)))

print("Formula:", serialize(phi))

# weight function definition
w = Ite(LE(y, Real(1)),
        Plus(x, y),
        Times(Real(2), y))

chi = Bool(True)

print("Weight function:", serialize(w))
print("Support:", serialize(chi))

wmi = MyWMI(chi, w)
print()
for mode in [wmipa.WMI.MODE_ALLSMT, wmipa.WMI.MODE_PA]:
    result, n_integrations = wmi.computeWMI(phi, mode=mode)
    print("WMI with mode {} \t result = {}, \t # integrations = {}".format(mode, result, n_integrations))
'''
# ================================================================================


# ================================================================================
#                                     Example 4
# ================================================================================

# variables definition
a = Symbol("A", BOOL)
b = Symbol("B", BOOL)
c = Symbol("C", BOOL)
x = Symbol("x", REAL)

# formula definition
phis = [Bool(True), Iff(a, Bool(True)), LE(x, Real(3))]

# weight function definition
w = Ite(a, x, Times(Real(2), x))

chi = And(GE(x, Real(5)), LE(x, Real(5)),
          Implies(a, GE(x, Real(0))),
          Implies(b, GE(x, Real(2))),
          Implies(c, LE(x, Real(3))))

print("Weight function:", serialize(w))
print("Support:", serialize(chi))

wmi = MyWMI(chi, w)

print()
for mode in [wmipa.WMI.MODE_ALLSMT, wmipa.WMI.MODE_PA]:
    for phi in phis:
        result, n_integrations = wmi.computeWMI(phi, mode=mode)
        print("Query: {}".format(serialize(phi)))
        print("WMI with mode {} \t result = {}, \t # integrations = {}".format(mode, result, n_integrations))

# ================================================================================


