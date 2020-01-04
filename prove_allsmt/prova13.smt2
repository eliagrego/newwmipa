(set-option :produce-models true)
(set-logic QF_LRA)

(declare-fun x () Real)
(declare-fun y () Real)

(declare-fun A1 () Bool)
(declare-fun A2 () Bool)
(declare-fun A3 () Bool)

(assert
(and
 (or A1 (not A1))
 (or A2 (not A2))
))

(check-allsat (A1 A2))



