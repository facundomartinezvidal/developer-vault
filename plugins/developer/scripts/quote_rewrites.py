"""Book passages in the vault notes, and the wording used instead in this public repo.

The vault is private and keeps the quotes. sync_vault.py applies these after rendering each
reference file. Keep this file identical in every plugin that syncs from the vault.
"""

import re

TIP_TITLE = re.compile(r'Tip (\d+), "[^"]+"')

REWRITES = [
    ('"the real key to making it easy to understand small functions is good naming... if you have a good name for a function, you mostly don\'t need to look at its body."', "and good names are what make that work, because a well-named function rarely needs its body read."),
    ('"all race conditions, deadlock conditions, and concurrent update problems are due to mutable variables. You cannot have a race condition or a concurrent update problem if no variable is ever updated."', "races, deadlocks and concurrent update bugs all need a variable that changes; if nothing is ever updated, they can't occur."),
    ('"The problem with global data is that it can be modified from anywhere in the code base, and there\'s no mechanism to discover which bit of code touched it" — leading to "spooky action at a distance" bugs', "Anything can change it and nothing records who did, which leads to bugs"),
    ('"the difference between a poison and something benign is the dose"', "how harmful it is depends on how much there is"),
    ('"if it\'s important enough to be global, wrap it in an API"', "if it must be global, put it behind an API"),
    ('"If it\'s important enough to be global, wrap it in an API"', "If it must be global, put it behind an API"),
    ('"Gather together those things that change at the same times and for the same reasons; separate those things that change at different times or for different reasons."', "Keep together what changes for the same reasons at the same times, and split apart what doesn't."),
    (' — "we\'ve lost count of the times we\'ve seen a function invoking half-a-dozen getter methods on another object to calculate some value."', ", typically by calling many getters on another object to compute a value."),
    (': "I have to change these three functions every time I get a new database; I have to change these four functions every time there\'s a new financial instrument."', ": some functions change for each new database, and others for each new financial instrument."),
    ('"If component A should be protected from changes in component B, then component B should depend on component A."', "To protect A from changes in B, make B depend on A."),
    ('Martin calls it "the most fundamental reason we study software architecture."', "Martin treats it as the core reason to study architecture."),
    (': "when you can\'t think of a good name for something, it\'s often a sign of a deeper design malaise."', ": struggling to name something often points to a design problem."),
    ('"one of the two hard things in programming,"', "one of the hardest things in programming,"),
    ('"a grouping of related functionality behind a nice clean interface, which resides inside an execution environment"', "related functionality behind a clear interface, running inside one execution environment"),
    ("a thing is well designed if it adapts to the people who use it", "good design is design that fits the people using it"),
    ('"that\'s particularly hard to spot if it only happens under rare conditions."', "that's hard to notice when it occurs only in rare conditions."),
    ('"oh, I think we\'ll need the ability to do this kind of thing someday,"', "code added because it might be needed someday,"),
    ('and "nine times out of ten this smell is too faint to be worth cleaning."', "and usually this smell is too weak to justify cleaning up."),
    ('"Architecture must be flexible enough to adapt to the size of the problem."', "Architecture has to fit the size of the problem."),
    ('and "when a class has too many fields, duplicated code cannot be far behind."', "and too many fields tend to bring duplicated code with them."),
    ('because "you expect an object to need all of its fields" — trying to figure out why a field exists when it doesn\'t seem to be used can drive you nuts.', "because readers assume that an object needs all of its fields, and then struggle to work out why this one exists."),
    ('"The difficulty in making a change should be proportional only to the scope of the change, not to its shape"', "The cost of a change should depend on how big it is, not on its shape"),
    ('"hard to find, and it\'s easy to miss an important change"', "easy to overlook, including important ones"),
    ('"The web is a detail. The database is a detail."', "The web and the database are details."),
    ('"modules that whisper to each other by the coffee machine,"', "modules informally sharing private knowledge,"),
    ('"in all languages, they are the granule of deployment."', "whatever the language, it's the smallest unit you deploy."),
    ('"a component should not have multiple reasons to change."', "a component should have one reason to change."),
    ('"testing shows the presence, not the absence, of bugs"', "tests can reveal bugs but can't prove there are none"),
    ('"Our applications are not CRUD; they are just CR."', "Applications then only create and read, never update or delete."),
    ('"consider deleting one of the data values — if the others don\'t make sense without it, that\'s a sure sign you have an object that\'s dying to be born."', "remove one of the values; if the rest stop making sense, they want to be an object of their own."),
    ('"Coding ain\'t done \'til all the tests run"', "Coding isn't finished until all the tests pass"),
    ('"pure business and nothing else"', "business rules only"),
    ("Architecture teams must not siphon off all the best and brightest", "Architecture teams must not take all the strongest people"),
    ("a good architect maximizes the number of decisions *not* made", "a good architect keeps as many decisions as possible open"),
    ("a good architect maximizes the number of decisions not made", "a good architect keeps as many decisions as possible open"),
    ("A good architect maximizes the number of decisions not made", "A good architect keeps as many decisions as possible open"),
    ("Align the model with the consistent aspects of the domain, the ones that make it a coherent area of knowledge in the first place.", "Fit the model to the stable parts of the domain, which are what hold it together as a subject."),
    ("Refactor the segregated core module to make its relationships and interactions simpler and more communicative.", "Simplify the relationships of the separated core, and make them clearer."),
    ("Refactor code to sever data and functionality that aren't directly part of the concept, putting it in other packages.", "Move data and functions that aren't part of the concept into other packages."),
    ("Architecture is defined by boundaries that separate high-level policy from low-level detail and obey", "Architecture comes from boundaries that keep policy apart from detail and follow"),
    ("Every system has at least one component that creates, coordinates, and oversees the others:", "Every system has a component that creates and coordinates the rest:"),
    ("A function that handles errors should do nothing else.", "Keep error handling in a function of its own."),
    ("Looks like it was written by someone who cares", "Shows that its author cared"),
    ("An **actor** is an independent virtual processor with its own *private* state and a mailbox.", "An **actor** is an independent unit of execution with private state and a mailbox."),
    ("each layer gives a *different* abstraction from the layers above and below it", "each layer offers its own abstraction, distinct from its neighbors"),
    ("each layer should provide a different abstraction from the layers above and below it", "each layer should offer its own abstraction, distinct from its neighbors"),
    ("the least likely to change when something external changes", "the least affected by external change"),
    ("is a set of high-level concepts or rules that establishes a pattern of design for the whole system.", "is a set of shared concepts or rules that shapes the design of the whole system."),
    ("An ill-fitting structure is worse than none.", "A structure that doesn't fit does more harm than having none."),
    ("Comments belong in the code, not the commit log.", "Put comments in the code instead of the commit log."),
    ('there\'s no such thing as an "object-relational mapper", because', "the name object-relational mapper misleads, because"),
    ("Build end-to-end, not top-down or bottom-up", "Build thin end-to-end slices, rather than top-down or bottom-up"),
    ("A test is **the first user of your code**", "A test is **your code's first caller**"),
    ("**the function or object that allocates a resource is responsible for deallocating it.**", "**whoever allocates a resource releases it.**"),
    ("be strict about what you accept, and promise as little as possible in return", "accept strictly and promise little"),
    ("Work with a user to think like a user", "Work alongside users to see things as they do"),
    ("work with a user to think like a user", "work alongside users to see things as they do"),
    ("**help people understand what they want**", "**help people discover what they need**"),
    ("if the common functions can combine their output for a later phase", "when their output can feed a later phase"),
    ("The three laws lock you into a cycle about 30 seconds long:", "The three laws are: write no production code without a failing test, write only enough of a test to fail, and write only enough code to pass it. They lock you into a cycle about 30 seconds long:"),
    ("Tests and production code are written together, with the tests a few seconds ahead.", "Tests come a few seconds before the code they cover."),
    ('"If component A should be protected from changes in component B, then component B should depend on component A"', "To protect A from changes in B, make B depend on A"),
    ("it's a heuristic: \"a metric is not a god.\"", "it's a heuristic, and shouldn't be followed blindly."),
    ('"frameworks are tools, not ways of life."', "frameworks should stay tools."),
    ('In Evans\'s words: "A model proposes; a COHESIVE MECHANISM disposes."', "As Evans puts it, the model states the problem and the mechanism solves it."),
    ('"for most applications, maintainability is more important than reusability."', "most applications need to be easy to maintain more than they need reuse."),
    ('duplication is "the root of all evil in software"', "duplication is the worst of the problems"),
    ('he\'s not "unconditionally opposed to the conditional."', "he has nothing against conditionals as such."),
    ('"threads should be as independent as possible"', "keep threads independent"),
    ('"treat spurious failures as candidate threading issues"', "suspect threading when failures look random"),
    ('"draw on established formalisms"', "reuse established formalisms"),
    ("If it's important enough to be global, wrap it in an API", "If it must be global, put it behind an API"),
]


def apply(text):
    for old, new in REWRITES:
        text = text.replace(old, new)
    return TIP_TITLE.sub(r"Tip \1", text)
