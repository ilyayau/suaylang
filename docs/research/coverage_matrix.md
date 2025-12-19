# Coverage Matrix

This matrix is generated from `conformance/manifest.json` and is intended to be reviewer-auditable.

- Corpus root: `conformance/corpus`
- Programs (fixed): 50

| Feature | Programs | VM support |
|---|---|---|
| `and` | `015_short_circuit.suay` | supported |
| `ascii_aliases` | `028_ascii_aliases.suay` | supported |
| `binary:%` | `002_arith_ops.suay` | supported |
| `binary:+` | `002_arith_ops.suay` | supported |
| `binary:×` | `002_arith_ops.suay` | supported |
| `binary:÷` | `002_arith_ops.suay`, `040_error_div_zero.suay` | supported |
| `binary:−` | `002_arith_ops.suay` | supported |
| `binding` | `009_mutation_ok.suay`, `035_binding_shadowing.suay` | supported |
| `block` | `017_nested_blocks.suay`, `035_binding_shadowing.suay` | supported |
| `builtin:at` | `037_list_take_drop_at.suay` | supported |
| `builtin:drop` | `037_list_take_drop_at.suay` | supported |
| `builtin:fold` | `026_map_fold_builtin.suay` | supported |
| `builtin:has` | `036_map_put_has_keys.suay` | supported |
| `builtin:map` | `026_map_fold_builtin.suay` | supported |
| `builtin:put` | `036_map_put_has_keys.suay` | supported |
| `builtin:say` | `002_arith_ops.suay` | supported |
| `builtin:take` | `037_list_take_drop_at.suay` | supported |
| `builtin:text` | `001_literals.suay` | supported |
| `call` | `004_lambda_closure.suay`, `018_lambda_two_args.suay`, `042_lambda_pattern_param_variant.suay`, `046_module_main_basic.suay` | supported |
| `closure` | `004_lambda_closure.suay`, `034_closure_captures_mutation.suay` | supported |
| `compare` | `002_arith_ops.suay`, `008_cycle_gcd.suay`, `033_cycle_state_machine_heavy.suay`, `038_text_compare_dispatch.suay` | supported |
| `concat` | `022_text_concat.suay` | supported |
| `continue` | `007_cycle_sum.suay` | supported |
| `currying` | `018_lambda_two_args.suay` | supported |
| `cycle` | `007_cycle_sum.suay`, `008_cycle_gcd.suay`, `013_cycle_no_match_error.suay`, `027_workflow_min.suay`, `028_ascii_aliases.suay`, `033_cycle_state_machine_heavy.suay` | supported |
| `dispatch` | `005_dispatch_variant.suay`, `006_dispatch_list_tail.suay`, `012_dispatch_no_match_error.suay`, `014_runtime_error_in_dispatch_arm.suay`, `019_dispatch_list_cases.suay`, `027_workflow_min.suay`, `028_ascii_aliases.suay`, `032_dispatch_tuple_deep.suay`, `033_cycle_state_machine_heavy.suay`, `038_text_compare_dispatch.suay`, `043_dispatch_list_tail_empty.suay`, `044_dispatch_variant_nested_payload.suay` | supported |
| `evaluation_order` | `031_eval_order_left_to_right.suay` | supported |
| `finish` | `007_cycle_sum.suay` | supported |
| `hashable_keys` | `023_map_keys_ok.suay`, `041_error_unhashable_map_key.suay` | supported |
| `import_cycle` | `049_module_cycle_a.suay`, `050_module_cycle_b.suay` | supported |
| `lambda` | `004_lambda_closure.suay`, `018_lambda_two_args.suay`, `028_ascii_aliases.suay`, `042_lambda_pattern_param_variant.suay`, `045_module_math.suay` | supported |
| `left_to_right` | `031_eval_order_left_to_right.suay` | supported |
| `lex_error` | `029_lex_error.suay` | supported |
| `lexical_scope` | `017_nested_blocks.suay` | supported |
| `link` | `045_module_math.suay`, `046_module_main_basic.suay`, `047_module_private_member_error.suay`, `048_module_missing_export_error.suay`, `049_module_cycle_a.suay`, `050_module_cycle_b.suay` | supported |
| `list` | `003_structures.suay`, `025_list_building.suay`, `037_list_take_drop_at.suay` | supported |
| `literals` | `001_literals.suay` | supported |
| `map` | `003_structures.suay`, `023_map_keys_ok.suay`, `036_map_put_has_keys.suay`, `041_error_unhashable_map_key.suay` | supported |
| `mod` | `008_cycle_gcd.suay`, `033_cycle_state_machine_heavy.suay` | supported |
| `modules` | `045_module_math.suay`, `046_module_main_basic.suay`, `047_module_private_member_error.suay`, `048_module_missing_export_error.suay`, `049_module_cycle_a.suay`, `050_module_cycle_b.suay` | supported |
| `mutation` | `009_mutation_ok.suay`, `010_mutation_error.suay`, `034_closure_captures_mutation.suay`, `039_short_circuit_side_effects.suay` | supported |
| `name` | `011_undef_name_error.suay`, `014_runtime_error_in_dispatch_arm.suay` | supported |
| `not` | `024_bool_not_truthiness.suay` | supported |
| `or` | `015_short_circuit.suay` | supported |
| `parse_error` | `030_parse_error.suay` | supported |
| `pattern:bool` | `038_text_compare_dispatch.suay` | supported |
| `pattern:grouping` | `020_tuple_patterns.suay` | supported |
| `pattern:list` | `006_dispatch_list_tail.suay`, `019_dispatch_list_cases.suay`, `043_dispatch_list_tail_empty.suay` | supported |
| `pattern:list_tail` | `006_dispatch_list_tail.suay`, `043_dispatch_list_tail_empty.suay` | supported |
| `pattern:tuple` | `020_tuple_patterns.suay`, `032_dispatch_tuple_deep.suay` | supported |
| `pattern:variant` | `005_dispatch_variant.suay`, `021_nested_variants.suay`, `032_dispatch_tuple_deep.suay`, `042_lambda_pattern_param_variant.suay`, `044_dispatch_variant_nested_payload.suay` | supported |
| `pattern:wildcard` | `005_dispatch_variant.suay` | supported |
| `runtime_error` | `010_mutation_error.suay`, `011_undef_name_error.suay`, `012_dispatch_no_match_error.suay`, `013_cycle_no_match_error.suay`, `014_runtime_error_in_dispatch_arm.suay`, `040_error_div_zero.suay`, `041_error_unhashable_map_key.suay`, `047_module_private_member_error.suay`, `048_module_missing_export_error.suay`, `049_module_cycle_a.suay`, `050_module_cycle_b.suay` | supported |
| `scope` | `009_mutation_ok.suay`, `034_closure_captures_mutation.suay`, `035_binding_shadowing.suay` | supported |
| `short_circuit` | `015_short_circuit.suay`, `039_short_circuit_side_effects.suay` | supported |
| `state_machine` | `027_workflow_min.suay`, `033_cycle_state_machine_heavy.suay` | supported |
| `text` | `001_literals.suay`, `022_text_concat.suay`, `038_text_compare_dispatch.suay` | supported |
| `truthiness` | `024_bool_not_truthiness.suay` | supported |
| `tuple` | `003_structures.suay`, `025_list_building.suay` | supported |
| `unary:¬` | `016_unary_ops.suay` | supported |
| `unary:−` | `016_unary_ops.suay` | supported |
| `variant` | `003_structures.suay`, `021_nested_variants.suay` | supported |

## How to regenerate

```sh
python -m tools.research.gen_coverage_matrix
```
