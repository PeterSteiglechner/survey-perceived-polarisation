#################################
#####  IMPORTANCE NOT COVERED QUESTIONS  #####
#################################
class slide10b_ImportanceOther(Page):
    form_model = "player"
    form_fields = [f"importance_{q}" for q in C.QUS_OTHERS] + [
        "importance_other_comments"
    ]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.current_page += 1

    @staticmethod
    def is_displayed(player: Player):
        trainingPassed = player.isTrainingPassed
        return player.consent and trainingPassed

    @staticmethod
    def vars_for_template(player):
        lan = player.language
        if player.field_maybe_none(f"t_on_importance_other") is None:
            player.t_on_importance_other = int(time.time())
        questions = (
            C.QUS_OTHERS
        )  # [C.QUS[i] for i in json.loads(player.question_sorting)]
        fields = [f"importance_{q}" for q in questions]
        questions = [C.QUESTIONS_OTHERS[player.language][q] for q in questions]

        field_question_pairs = []
        for field, question in zip(fields, questions):
            field_question_pairs.append(
                {
                    "field_name": field,
                    "question_text": question,
                    "first_label": (
                        "no influence at all"
                        if lan == "en"
                        else "überhaupt kein Einfluss"
                    ),
                    "last_label": (
                        "very strong influence"
                        if lan == "en"
                        else "sehr starker Einfluss"
                    ),
                }
            )
        return {
            "maxslides": C.MAXSLIDES,
            "nslide": player.current_page,
            "lan_en": lan == "en",
            "field_question_pairs": field_question_pairs,
            "page_title": (
                "Relevance of Issues not Considered"
                if lan == "en"
                else "Relevanz nicht berücksichtigter Themen"
            ),
            "table_head": (
                "Influence of additional issues on your perception of political differences and similarities"
                if lan == "en"
                else "Einfluss zusätzlicher politischer Themen auf Ihre Wahrnehmung politischer Differenzen und Ähnlichkeit"
            ),
            "pretext": (
                "For this survey, we have selected four political questions that cover a broad spectrum of issues and have long been present in public debate. Of course, four questions cannot fully reflect your political worldview or that of other people. Below, we present four additional questions."
                if lan == "en"
                else "Für diese Umfrage haben wir vier politische Fragen ausgewählt, die ein breites Spektrum an Themen abdecken und seit langem in der öffentlichen Debatte präsent sind. Natürlich können vier Fragen nicht Ihr politisches Weltbild oder das anderer Personen vollständig widerspiegeln. Im Folgenden zeigen wir Ihnen vier zusätzliche Fragen."
            ),
            "question": (
                "Please rate the extent to which the following additional questions would have changed your placement of the various individuals on your political map.<br>Would the question have had little influence or a strong influence on your political map and changed the positions of the individuals?"
                # "Please rate <b>how important</b> each of these additional questions <b>would have been</b> to you personally for the last two tasks (creating the political map and evaluating the pairs of individuals), if we had asked them in addition!"
                if lan == "en"
                else "Bitte schätzen Sie, inwieweit die folgenden zusätzlichen Fragen jeweils Ihre Anordnung der verschiedenen Personen auf Ihner politischen Landkarte verändert hätten.<br>Hätte die Frage keinen großen Einfluss, oder einen starken Einfluss auf Ihre politische Karte gehabt und die Positionen der Personen verändert?"
                # "Bitte schätzen Sie ein, <b>wie wichtig</b> diese zusätzlichen politischen Fragen jeweils für Sie <b>gewesen wären</b> für die Bearbeitung der letzten beiden Aufgaben (die politische Karte zu erstellen bzw. einzelne Paare zu bewerten), wenn wir die Fragen zusätzlich gestellt hätten!"
            ),
            "explain_text": (
                "If you want, you can explain here in more detail how these additional questions would have influenced you or not influenced you <em>(optional)</em>:"
                if lan == "en"
                else "Wenn Sie wollen, können Sie hier näher erklären, wie diese zusätzlichen Fragen Sie beeinflusst oder nicht beeinflusst hätten <em>(optional)</em>:"
            ),
        }
