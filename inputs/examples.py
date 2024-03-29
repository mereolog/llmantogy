SAMPLE_FORMALISATIONS = \
{
'There is a four-legged table made of wood. Some time later, a leg of the table is replaced. Even later, the table is demolished so it ceases to exist although the wood is still there after the demolition.' :
"""(if (Artefact x) (PhysicalObject x))
(if (Table x) (Artefact x))
(if (Tabletop x) (Artefact x))
(if (Leg x) (Artefact x))
(if (Wood x) (Matter x))
(Table ta)
(Tabletop tt)
(Leg L1)
(Leg L2)
(Leg L3)
(Leg L4)
(Leg L4Replace)
(Wood ttw)
(Wood W1)
(Wood W2)
(Wood W3)
(Wood W4)
(Wood W4Replace)
(Time t1)
(Time t2)
(Time t3)
(< t1 t2)
(< t2 t3)
(present ta t1)
(present ta t2)
(present tt t1)
(present tt t2)
(present L1 t1)
(present L2 t1)
(present L3 t1)
(present L4 t1)
(present L1 t2)
(present L2 t2)
(present L3 t2)
(present L4Replace t2)
(present W1 t1)
(present W2 t1)
(present W3 t1)
(present W4 t1)
(present W1 t2)
(present W2 t2)
(present W3 t2)
(present W4Replace t2)
(present W1 t3)
(present W2 t3)
(present W3 t3)
(present W4Replace t3)
(not (present ta t3))
(not (present L1 t3))
(not (present L2 t3))
(not (present L3 t3))
(not (present L4Replace t3))
(part(tt ta (+ t1 t2)))
(part(L1 ta t1))
(part(L2 ta t1))
(part(L3 ta t1))
(part(L4 ta t1))
(part(L1 ta t2))
(part(L2 ta t2))
(part(L3 ta t2))
(part(L4Replace ta t2))
(not (part(L4 ta t2)))
(constitute (ttw tt (+ t1 t2)))
(constitute(W1 L1 t1))
(constitute(W2 L2 t1))
(constitute(W3 L3 t1))
(constitute(W4 L4 t1))
(constitute(W1 L1 t2))
(constitute(W2 L2 t2))
(constitute(W3 L3 t2))
(constitute(W4Replace L4Replace t2))
""",
'A man is walking to the station, but before he gets there, he turns around and goes home.' :
"""
(if (Person x) (AgentivePhysicalObject x))
(if (SpeedQuality x) (TemporalQuality x))
(if (Walk x) (Process x))
(if (Turn x) (Accomplishment x))
(if (Plan x) (Concept x))
(Person a)
(Perdurant e)
(Walk e1)
(Turn e2)
(Walk e3)
(Plan p1)
(Plan p2)
(Time te1)
(Time te2)
(Time te3)
(< te1 te2)
(< te2 te3)
(temporalquale te1 e1)
(temporalquale te2 e2)
(temporalquale te3 e3)
(present a te)
(present p1 te1)
(present p2 te2)
(present p2 te3)
(not (present p1 te2))
(not (present p1 te3))
(not (present p2 te1))
(if (executes_plan x y) (and (Perdurant x) (Concept y)))
(DirectionQuality s)
(quality s e)
(quale l1 s te1)
(quale l2 s te2)
(quale l3 s te3)
(quale l1 s t2i)
(quale l3 s t2f)
(not (= l1 l3))
(= e (+ e1 e2 e3))
(participates_constantly a e)
(executes_plan e1 p1)
(executes_plan (+ e2 e3) p2)
(if (and (SpeedQuality s) (quality s x) (Walk x)) (forall (li lj ti tj) (if (and (quale li s ti) (quale lj s tj) (part ti tx) (part tj tx)) (= li lj))))
(if (and (DirectionQuality s) (quality s y) (Turn y) (quale l1 s tyi) (quale l3 s tyf) (< ti tj) (< l1 l3) (part ti ty) (part tj ty) (quale li s ti) (quale lj s tj) (= (+ li ri) (+ lj rj)) (= (+ lj rj) l3)) (and (<= 0 rj) (< rj ri)))
""",
'Mr. Potter is the teacher of class 2C at Shapism School and resigns at the beginning of the spring break. After the spring break, Mrs. Bumblebee replaces Mr. Potter as the teacher of 2C. Also, student Mary left the class at the beginning of the break and a new student, John, joins in when the break ends.' :
"""
(if (Person x) (AgentivePhysicalObject x))
(if (FunctionalRole x) (Role x))
(if (Role x) (NonAgentiveSocialObject x))
(if (and (FunctionalRole x) (classify x y t) (classify x1 y t1) ) (= x x1))
(Person Potter)
(Person Bumblebee)
(Person Mary)
(Person John)
(Role 2CStudent)
(FunctionalRole 2CTeacher)
(not (FunctionalRole 2CStudent))
(Time t1)
(Time t2)
(Time t3)
(< t1 t2)
(< t2 t3)
(present Potter t1)
(present Bumblebee (+ t2 t3))
(present Mary t1)
(present John t3)
(forall (x) (not (classify x 2CTeacher t2)))
(classify Potter 2CTeacher t1)
(classify Bumblebee 2CTeacher t3)
(classify Mary 2CStudent t1)
(not (classify John 2CStudent t1))
(not (classify Mary 2CStudent t2))
(not (classify John 2CStudent t2))
(not (classify Mary 2CStudent t3))
(classify John 2CStudent t3)
""",
'A flower is red in the summer. As time passes, the color changes. In autumn the flower is brown.':
"""
(if (Flower x) (PhysicalObject x))
(if (ColorQuality x) (PhysicalQuality x))
(if (cc x) (PhysicalRegion x))
(Flower f)
(ColorQuality cq)
(Time s)
(Time a)
(Time t0)
(Time t1)
(present f s)
(present f a)
(quality cq f)
(quale fc0 cq t0)
(part t0 s)
(quale fc1 cq t1)
(part t1 a)
(part fc0 rr)
(part fc1 br)
(part rr ColorSpace)
(part br ColorSpace)
(< s a)
(exists (p) (and (SelfConnected p) (part p cc) (part fc0 p) (part fc1 p) (forall (l) (if (part l p) (exists (t) (and (part t (+ s a))(quality l cq)))))))
""",
'Marriage is a contract between two people that is present in most social and cultural systems and it can change in major (e. g. gender constraints) and minor (e.g. marriage breaking procedures) aspects.':
"""
(if (SocialMarriage x) (Concept x))
(if (LegalMarriage x) (Concept x))
(if (SocialRelationship x) (SocialObject x))
(SocialRelationship m)
(SocialMarriage sm)
(LegalMarriage lm)
(LegalMarriage lm1)
(Time t)
(Time t1)
(present m t)
(present m t1)
(present sm t)
(present sm t1)
(present lm t)
(not (present lm t1))
(not (present lm1 t))
(present lm1 t1)
(not (= lm1 lm2))
(if (classify sm m t) (classify lm m t))
(if (classify sm m t1) (classify lm1 m t1))""",
'A man is walking when suddenly he starts walking faster and then breaks into a run.':
"""
(if (Person x) (AgentivePhysicalObject x))
(if (SpeedQuality x) (TemporalQuality x))
(if (SpeedQSpace x) (TemporalRegion x))
(if (Walk x) (Process x))
(if (Run x) (Process x))
(if (SpeedUp x) (Accomplishment x))
(Person a)
(Perdurant e)
(Walk e1)
(SpeedUp e2)
(Run e3)
(SpeedQuality s)
(SpeedQuality s1)
(SpeedQuality s2)
(SpeedQuality s3)
(Time te)
(Time te1)
(Time te2)
(Time te3)
(present a te)
(part l SpeedSpace)
(part l1 SpeedSpace)
(part l2 SpeedSpace)
(part l3 SpeedSpace)
(quality s e)
(quality l s te)
(quality s1 e1)
(quality l1 s1 te1)
(quality s2 e2)
(quality l2 s2 te2)
(quality s3 e3)
(quality l3 s3 te3)
(= e (+ e1 e2 e3))
(participates_constantly p e)
(if (and (quality s x) (or (Walk x) (Run x)))(forall (li lj ti tj)(if (and (quale li s ti) (quale lj s tj) (part ti tx) (part tj tx))(= li lj))))
(if (and (quality s x) (SpeedUp x)) (exists (li lj tj tj) (and (part ti tx) (part tj tx) (quale li s ti) (quale lj s tj) (not (= li lj)) (forall (li lj ti tj) (if (and (part ti tx) (part tj tx) (quale li s ti) (quale lj s tj)) (iff (<= li lj) (< ti tj)))))))
"""
}