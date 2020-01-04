(set-option :produce-models true)
(set-logic QF_LRA)

(declare-fun x () Real)
(declare-fun y () Real)
(declare-fun z () Real)
(declare-fun w () Real)
(declare-fun v () Real)

(declare-fun A1 () Bool)
(declare-fun A2 () Bool)
(declare-fun A3 () Bool)

(assert
 (and
  (or A1 A2     (= y (+ 1 x)))
  (or A1 (not A2)     (= y (+ 2 z)))
  (or (not A1) A2     (= y (+ 3 w)))
  (or (not A1) (not A2)     (= y (+ 4 v)))
 )
)


(check-allsat (A1 A2))



