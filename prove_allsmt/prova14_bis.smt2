(declare-fun x () Int)
(declare-fun y () Int)

(declare-fun a () Bool)
(declare-fun b () Bool)
(declare-fun c () Bool)
(declare-fun d () Bool)

(assert (= (> x 0) a))
(assert (= (> y 0) b))


;; enumerate all the consistent assignments (i.e. solutions) for the given
;; list of predicates. Notice that the arguments to check-allsat can only be
;; Boolean constants. If you need to enumerate over arbitrary theory atoms,
;; you can always "label" them with constants, as done above for
;; "(> (+ x y) 0)", labeled by "a"
(check-allsat ((> x 0) (> y 0)))

(exit)
