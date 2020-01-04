(set-option :produce-models true)
(set-logic QF_LRA)

(declare-fun x () Real)
(declare-fun y () Real)

(declare-fun A1 () Bool)
(declare-fun A2 () Bool)
(declare-fun A3 () Bool)
(declare-fun A4 () Bool)

(assert
 (= y
   (ite A1
     (ite A2
       (* 1 x)
       (* 2 x)
     )
     (ite A3
       (* 3 x)
       (* 4 x)
     )
   )
))

(check-allsat (A1 A2 A3))
