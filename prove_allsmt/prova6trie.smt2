(set-option :produce-models true)
(set-logic QF_UFLRA)

(declare-fun x () Real)
(declare-fun y () Real)

(declare-fun fmul (Real Real) Real)

(declare-fun A1 () Bool)
(declare-fun A2 () Bool)
(declare-fun A3 () Bool)
(declare-fun A4 () Bool)

(assert (>= x 0))
(assert (<= x 1))

(assert
 (and
  (or (not A1) (= y (fmul x x)))
  (or A1
      (and
       (or (not A2) (= y (fmul x (* 2 x))))
       (or A2 
           (and
            (or (not A3) (= y (* 3 x)))
            (or A3  (= y (* 4 x)))
)))   ))   )

;; equivalente a 
;; (assert
;;  (= y
;;    (ite A1
;;      x
;;      (ite A2
;;        (* 2 x)
;;        (ite A3
;;           (* 3 x)
;; 	  (* 4 x)
;; )) ) ) )

(check-allsat (A1 A2 A3))
