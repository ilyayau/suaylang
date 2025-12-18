# Decision log (1..1000)

This table is the contract-driven mapping from deficiency item → decision → normative reference → enforcing tests.

In v0.1, ‘fixing’ a deficiency means: specify precisely, forbid with a diagnostic, or declare out-of-scope with a gate.



| # | Category | Decision | Reference | Tests | Compatibility |
|---:|---|---|---|---|---|
| 1 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 2 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 3 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 4 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 5 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 6 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 7 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 8 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 9 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 10 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 11 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 12 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 13 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 14 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 15 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 16 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 17 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 18 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 19 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 20 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 21 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 22 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 23 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 24 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 25 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 26 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 27 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 28 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 29 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 30 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 31 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 32 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 33 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 34 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 35 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 36 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 37 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 38 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 39 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 40 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 41 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 42 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 43 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 44 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 45 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 46 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 47 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 48 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 49 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 50 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 51 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 52 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 53 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 54 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 55 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 56 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 57 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 58 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 59 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 60 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 61 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 62 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 63 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 64 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 65 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 66 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 67 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 68 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 69 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 70 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 71 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 72 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 73 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 74 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 75 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 76 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 77 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 78 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 79 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 80 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 81 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 82 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 83 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 84 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 85 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 86 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 87 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 88 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 89 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 90 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 91 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 92 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 93 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 94 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 95 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 96 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 97 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 98 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 99 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 100 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 101 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 102 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 103 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 104 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 105 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 106 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 107 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 108 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 109 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 110 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 111 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 112 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 113 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 114 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 115 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 116 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 117 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 118 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 119 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 120 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 121 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 122 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 123 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 124 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 125 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 126 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 127 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 128 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 129 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 130 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 131 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 132 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 133 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 134 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 135 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 136 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 137 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 138 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 139 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 140 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 141 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 142 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 143 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 144 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 145 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 146 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 147 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 148 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 149 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 150 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 151 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 152 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 153 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 154 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 155 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 156 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 157 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 158 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 159 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 160 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 161 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 162 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 163 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 164 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 165 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 166 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 167 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 168 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 169 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 170 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 171 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 172 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 173 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 174 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 175 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 176 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 177 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 178 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 179 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 180 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 181 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 182 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 183 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 184 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 185 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 186 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 187 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 188 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 189 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 190 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 191 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 192 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 193 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 194 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 195 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 196 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 197 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 198 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 199 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 200 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 201 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 202 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 203 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 204 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 205 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 206 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 207 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 208 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 209 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 210 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 211 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 212 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 213 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 214 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 215 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 216 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 217 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 218 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 219 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 220 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 221 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 222 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 223 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 224 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 225 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 226 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 227 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 228 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 229 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 230 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 231 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 232 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 233 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 234 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 235 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 236 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 237 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 238 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 239 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 240 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 241 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 242 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 243 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 244 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 245 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 246 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 247 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 248 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 249 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 250 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 251 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 252 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 253 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 254 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 255 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 256 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 257 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 258 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 259 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 260 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 261 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 262 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 263 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 264 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 265 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 266 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 267 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 268 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 269 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 270 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 271 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 272 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 273 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 274 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 275 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 276 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 277 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 278 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 279 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 280 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 281 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 282 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 283 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 284 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 285 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 286 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 287 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 288 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 289 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 290 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 291 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 292 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 293 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 294 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 295 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 296 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 297 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 298 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 299 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 300 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 301 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 302 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 303 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 304 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 305 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 306 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 307 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 308 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 309 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 310 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 311 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 312 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 313 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 314 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 315 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 316 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 317 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 318 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 319 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 320 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 321 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 322 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 323 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 324 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 325 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 326 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 327 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 328 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 329 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 330 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 331 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 332 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 333 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 334 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 335 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 336 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 337 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 338 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 339 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 340 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 341 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 342 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 343 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 344 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 345 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 346 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 347 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 348 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 349 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 350 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 351 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 352 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 353 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 354 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 355 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 356 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 357 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 358 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 359 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 360 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 361 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 362 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 363 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 364 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 365 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 366 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 367 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 368 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 369 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 370 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 371 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 372 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 373 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 374 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 375 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 376 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 377 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 378 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 379 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 380 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 381 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 382 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 383 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 384 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 385 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 386 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 387 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 388 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 389 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 390 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 391 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 392 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 393 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 394 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 395 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 396 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 397 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 398 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 399 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 400 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 401 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 402 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 403 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 404 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 405 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 406 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 407 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 408 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 409 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 410 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 411 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 412 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 413 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 414 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 415 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 416 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 417 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 418 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 419 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 420 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 421 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 422 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 423 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 424 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 425 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 426 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 427 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 428 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 429 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 430 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 431 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 432 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 433 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 434 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 435 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 436 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 437 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 438 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 439 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 440 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 441 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 442 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 443 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 444 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 445 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 446 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 447 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 448 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 449 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 450 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 451 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 452 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 453 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 454 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 455 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 456 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 457 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 458 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 459 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 460 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 461 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 462 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 463 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 464 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 465 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 466 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 467 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 468 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 469 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 470 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 471 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 472 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 473 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 474 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 475 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 476 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 477 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 478 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 479 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 480 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 481 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 482 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 483 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 484 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 485 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 486 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 487 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 488 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 489 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 490 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 491 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 492 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 493 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 494 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 495 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 496 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 497 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 498 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 499 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 500 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 501 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 502 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 503 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 504 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 505 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 506 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 507 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 508 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 509 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 510 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 511 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 512 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 513 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 514 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 515 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 516 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 517 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 518 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 519 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 520 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 521 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 522 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 523 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 524 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 525 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 526 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 527 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 528 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 529 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 530 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 531 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 532 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 533 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 534 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 535 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 536 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 537 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 538 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 539 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 540 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 541 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 542 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 543 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 544 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 545 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 546 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 547 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 548 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 549 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 550 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 551 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 552 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 553 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 554 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 555 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 556 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 557 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 558 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 559 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 560 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 561 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 562 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 563 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 564 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 565 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 566 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 567 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 568 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 569 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 570 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 571 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 572 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 573 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 574 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 575 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 576 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 577 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 578 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 579 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 580 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 581 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 582 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 583 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 584 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 585 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 586 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 587 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 588 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 589 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 590 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 591 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 592 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 593 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 594 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 595 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 596 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 597 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 598 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 599 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 600 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 601 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 602 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 603 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 604 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 605 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 606 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 607 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 608 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 609 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 610 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 611 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 612 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 613 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 614 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 615 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 616 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 617 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 618 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 619 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 620 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 621 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 622 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 623 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 624 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 625 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 626 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 627 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 628 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 629 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 630 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 631 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 632 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 633 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 634 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 635 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 636 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 637 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 638 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 639 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 640 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 641 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 642 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 643 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 644 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 645 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 646 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 647 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 648 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 649 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 650 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 651 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 652 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 653 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 654 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 655 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 656 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 657 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 658 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 659 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 660 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 661 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 662 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 663 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 664 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 665 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 666 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 667 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 668 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 669 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 670 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 671 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 672 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 673 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 674 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 675 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 676 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 677 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 678 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 679 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 680 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 681 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 682 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 683 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 684 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 685 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 686 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 687 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 688 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 689 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 690 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 691 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 692 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 693 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 694 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 695 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 696 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 697 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 698 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 699 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 700 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 701 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 702 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 703 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 704 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 705 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 706 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 707 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 708 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 709 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 710 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 711 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 712 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 713 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 714 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 715 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 716 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 717 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 718 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 719 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 720 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 721 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 722 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 723 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 724 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 725 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 726 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 727 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 728 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 729 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 730 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 731 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 732 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 733 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 734 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 735 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 736 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 737 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 738 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 739 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 740 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 741 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 742 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 743 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 744 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 745 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 746 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 747 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 748 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 749 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 750 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 751 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 752 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 753 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 754 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 755 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 756 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 757 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 758 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 759 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 760 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 761 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 762 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 763 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 764 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 765 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 766 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 767 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 768 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 769 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 770 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 771 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 772 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 773 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 774 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 775 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 776 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 777 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 778 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 779 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 780 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 781 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 782 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 783 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 784 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 785 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 786 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 787 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 788 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 789 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 790 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 791 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 792 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 793 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 794 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 795 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 796 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 797 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 798 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 799 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 800 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 801 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 802 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 803 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 804 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 805 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 806 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 807 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 808 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 809 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 810 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 811 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 812 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 813 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 814 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 815 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 816 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 817 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 818 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 819 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 820 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 821 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 822 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 823 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 824 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 825 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 826 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 827 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 828 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 829 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 830 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 831 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 832 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 833 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 834 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 835 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 836 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 837 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 838 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 839 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 840 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 841 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 842 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 843 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 844 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 845 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 846 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 847 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 848 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 849 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 850 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 851 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 852 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 853 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 854 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 855 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 856 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 857 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 858 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 859 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 860 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 861 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 862 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 863 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 864 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 865 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 866 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 867 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 868 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 869 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 870 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 871 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 872 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 873 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 874 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 875 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 876 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 877 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 878 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 879 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 880 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 881 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 882 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 883 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 884 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 885 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 886 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 887 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 888 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 889 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 890 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 891 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 892 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 893 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 894 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 895 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 896 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 897 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 898 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 899 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 900 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 901 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 902 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 903 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 904 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 905 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 906 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 907 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 908 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 909 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 910 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 911 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 912 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 913 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 914 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 915 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 916 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 917 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 918 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 919 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 920 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 921 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 922 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 923 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 924 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 925 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 926 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 927 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 928 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 929 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 930 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 931 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 932 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 933 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 934 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 935 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 936 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 937 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 938 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 939 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 940 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 941 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 942 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 943 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 944 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 945 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 946 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 947 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 948 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 949 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 950 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 951 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 952 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 953 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 954 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 955 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 956 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 957 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 958 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 959 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 960 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 961 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 962 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 963 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 964 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 965 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 966 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 967 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 968 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 969 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 970 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 971 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 972 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 973 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 974 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 975 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 976 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 977 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 978 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 979 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 980 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 981 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 982 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 983 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 984 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 985 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 986 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 987 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 988 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 989 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 990 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |
| 991 | lexical | Specified | docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure | tests/README.md | Compatible |
| 992 | grammar | Specified | docs/reference/OPERATOR_TABLE.md#precedence-and-associativity | tests/test_parser.py | Compatible |
| 993 | evaluation | Specified | docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model | tools/conformance/run.py | Compatible |
| 994 | types_values | Specified | docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types | tests/test_runtime_primitives.py | Compatible |
| 995 | binding_scope | Specified | docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation | tests/test_interpreter.py | Compatible |
| 996 | control_flow | Specified | docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions | conformance/corpus | Compatible |
| 997 | collections | Specified | docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics | tests/test_runtime_primitives.py | Compatible |
| 998 | numbers_strings | Specified | docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model | tests/test_runtime_primitives.py | Compatible |
| 999 | errors_diagnostics | Specified | docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer | tests/test_golden_error_codes.py | Compatible |
| 1000 | modules_versioning | Out-of-scope (v0.1.x) | docs/reference/LANGUAGE_REFERENCE.md#12-modules | tests/test_modules.py | Compatible |

