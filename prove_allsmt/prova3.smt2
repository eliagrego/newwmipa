(set-option :produce-models true)
(set-logic QF_LRA)

(declare-fun x () Real)

(declare-fun A () Bool)
(declare-fun B () Bool)

(assert (or A (<= x 1)))
(assert (or (not A) (<= x 1)))
(assert (<= x 1))
;;(assert (>= x 0))

;;(assert (= B A))


(check-allsat (B))
