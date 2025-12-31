# Observability in a Machine Learning System: I Was Wrong from the Start

For a long time, I integrated machine learning components as first-class elements of the systems I was building, sometimes adding more logs and metrics to ensure their behavior conformed to a certain norm. This often meant defining heuristics or business rules to surface what I considered “strange” model behaviors and attempting to observe them.

In hindsight, I think this was a fundamental mistake.

---

## The Model: Just Another User

> The model is not the system.
>
> * it is not deterministic
> * it has no business invariants
> * it does not violate any explicit rule when it gets things wrong
> * it cannot be “buggy” in the software sense

> The model is a user of the system.
>
> * It consumes inputs.
> * It produces proposals.

Just like a human, an external API, or a third-party service.

You don’t observe a user.
You observe **what the system does with that user’s actions**.

---

## Silent Failure Is Not a Model Problem

A **silent failure** corresponds to an action taken by the model within the system that does not guarantee optimal service quality, while producing neither a technical error nor an explicit signal.

In many cases, the system deliberately delegates a decision to the model, accepting a degree of uncertainty. When the task at hand cannot be expressed deterministically—natural language understanding, semantic classification, contextual analysis—the model is often the best, or even the only, viable solution.

For a long time, I tried to introduce deterministic safeguards in the code to constrain the model and raise alerts. But it is important to understand that the entire field of machine learning was developed precisely because such rules were too restrictive. No explicit rule can replace a model robust enough to be used in production.

Silent failure is therefore not something observability should try to eliminate.
It is an intrinsic property of machine learning systems.

---

## So How Can Observability Ensure Service Quality?

It cannot. And it should not pretend to.

Error is inherent to machine learning. It is part of the trade-off accepted when delegating a non-deterministic task to a statistical model. That is precisely why it is healthier to treat the model as an external agent to the system, and to explicitly assume the risk this delegation entails.

Some models are nevertheless able to produce, in addition to a prediction, **statistical signals** such as confidence scores, uncertainty estimates, or class probabilities. These signals can be useful—not to judge the intrinsic quality of a prediction, but to qualify the context in which it was produced.

When used correctly, notions of uncertainty are not meant to automatically detect “bad” predictions. They allow the system to recognize that it is operating in a zone of doubt, and to accept the consequences: accepting the risk, triggering a human review, or simply recording that uncertainty as a business-relevant signal.

Observability therefore does not allow us to correct predictions after the fact, nor to reliably identify which ones are wrong. Trying to use it for that purpose would be a confusion of roles.

What observability *does* allow is making visible the **real business impact** of decisions made based on model predictions: effects on users, on workflows, on delays, on costs, or on key service-level indicators.

The fine-grained identification of prediction errors, their qualification, and their correction belong to another part of the system: manual annotation and human feedback.
It is this feedback loop—deliberately kept separate from observability—that enables the model to improve over time.

Observability does not improve the intrinsic quality of predictions.
It simply ensures that we never lose sight of their consequences—and of the level of uncertainty with which they were accepted.

---

## Conclusion

For a long time, I tried to make models observable.
I now believe that was the wrong battle.

Observability in a machine learning system is not about understanding what the model does, but about **making explicit how its outputs are used**.

The model proposes.
The system decides.
And observability should only concern what is explicit, deterministic, and accountable.
