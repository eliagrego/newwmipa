(set-option :produce-models true)
(set-logic QF_LRA)
(declare-fun x () Real)
(declare-fun y () Real)
(declare-fun A1 () Bool)
(declare-fun A2 () Bool)
(declare-fun A3 () Bool)

(assert
 (and
  (=> (and A1 A2)       (= y (* 1 x)))
  (=> (and A1 (not A2)) (= y (* 2 x)))
  (=> (and (not A1) A3)       (= y (* 3 x)))
  (=> (and (not A1) (not A3)) (= y (* 4 x)))
 )
)
(check-allsat (A1 A2 A3))
