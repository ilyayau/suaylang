# Memory model

This is an implementation-independent view of memory relevant to semantics.

- Values are immutable except for collections and environment bindings.
- Environments form a parent chain.
- Closures capture environments by reference.

This model is sufficient for the equivalence claim as long as observations do not include object identity.
