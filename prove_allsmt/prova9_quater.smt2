(set-option :produce-models true)
(set-logic QF_LRA)

(declare-fun x1 () Real)
(declare-fun x2 () Real)
(declare-fun x3 () Real)
(declare-fun x4 () Real)
(declare-fun x () Real)
(declare-fun y () Real)

(assert
 (let
  (
   (A1 (> x1 0))
   (A2 (> x2 0))
   (A3 (> x3 0))
  )
  (and
   (=> (and A1 A2)       (= y (* 1 x)))
   (=> (and A1 (not A2)) (= y (* 2 x)))
   (=> (and (not A1) A3)       (= y (* 3 x)))
   (=> (and (not A1) (not A3)) (= y (* 4 x)))
  )
 )
)

(check-allsat (A1 A2 A3))



