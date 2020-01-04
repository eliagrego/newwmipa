(set-option :produce-models true)
(set-logic QF_LRA)

(declare-fun x1 () Real)
(declare-fun x2 () Real)

(declare-fun A1 () Bool)
(declare-fun B1 () Bool)
(declare-fun B2 () Bool)

(assert (= B1 (> x1 1)))
(assert (= A1 (> x1 0)))
(assert (= B2 (< x2 3)))
(assert A1)
(assert (=> A1 B1))

(assert (or B1 B2))

(check-allsat (A1 B1 B2))
