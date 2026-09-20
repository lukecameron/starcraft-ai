# Kestrel hill-climb v19 result

Date: 2026-09-21  
Decision: **INCONCLUSIVE**

The registered v19 screen did not reach game initialization. It remains an
infrastructure-invalid, inconclusive result and is not gameplay, strength,
BASIL, Elo, submission, ladder, or tournament evidence. Do not rerun, reseed,
replace, or reinterpret v19.

## Frozen identity audit

The committed plan hash is
`4e4e24d05914ed9182aa7647489a3e60566f6c7e01041921b175a3b5ec2ea09f` and the
committed schedule hash is
`f4ba8bc3a42dc3b6a072e4295a217ae823a42ca05bce7695f4a827b5277913de`.
The runner-preserved schedule copy hashes to
`4e645cc0c9cf3946ada05fccc0efcb9ba63236df202053680987f6b2f6229f99`.
The runner manifest hashes to
`f58c735255d12893edf2ef6c4eeae277b41075fb941e8df9917654d486f31577`.

All 25 frozen identity checks pass: the v40 candidate, four opponent binaries,
launcher and sidecar, engine library, three runtime MPQs, four maps, provenance
registry, two patches, build sidecar, runner scripts, and plan hash all match
the registered schedule. The candidate binary is
`adac4ff4dc5aea71b94a5a12d13d62f964fe56a71ca3fd5141f24d0094401012`; the
engine library
`artifacts/builds/eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b/openbw-terminal-drain/libOpenBWData.dylib`
matches SHA-256 `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`.

## Preserved evidence

Rows 1–5 started concurrently at approximately 19:57:49Z and ended after
0.210–0.234 seconds. Each runner returned code 1 and was classified
`missing_or_inconsistent_metadata`; each had null logical-frame count and no
result metadata. The five child run manifests are preserved under
`artifacts/runs/20260920T195749-{c35a6e7e8bee,19b55228cc0b,7cf1dc87e980,8cba5d75f4e7,7e23b02145ce}/game-0001/manifest.json`.
Their SHA-256 hashes, in row order, are:

| Row | Run manifest SHA-256 | Runner stdout SHA-256 |
|---:|---|---|
| 1 | `d6c6edcafaea08c77774d73fc58b0f423145e92a5d6956f1093376a717f92e06` | `67f5090644b1ef906d50c3c10b2afc7eefb1f037e45b6c6c64bb179676412ce2` |
| 2 | `3396832e5eea334130217d6816f43ef7112a0f6aeb6d681572a4177201352c95` | `872f94e71b14fb62e5880955f7863795ae4e2a8ab4b724d9a65c4758b6c43369` |
| 3 | `5cdc59feaeb3ea461aee45c68dc75186852874276e0602bc9c637d61010c844c` | `0a7ea31a840514ab740e46377a407b5c8e7ddf24976d72caae266587ed9ee321` |
| 4 | `82cd6153f0e9285c5523e03a223dcdad2b4a8ba89eaafbcf911c9b41161e995d` | `4c9a6ee4d07d44163612c7364a28d973532e72bb2cc871915c6776da672eb4e0` |
| 5 | `3b0d4f627f378c105a622feb90449952f551f7887cd9baa0c6cc52e6e9fbb7a7` | `9997b94b0834192d88a10970a14aa823cac4b2cad2ea64e7ffbf1edbad753a9b` |

Every child stdout is exactly `Error: connect: No such file or directory.\n`
(SHA-256 `1661e40660285eebbf8be536989727cb2f57b43c36a9aedc4dcbc7bf5b16d39d`);
all child stderr files are empty (SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). No
replay, logical frame, terminal result, telemetry, or gameplay observation
exists. Rows 6–10 are explicit `skipped` entries classified
`stopped_after_repeated_infrastructure_failure`.

The failure is consistent with the restricted-sandbox LOCAL-socket launch
environment. v20 therefore requires unsandboxed execution before any row is
started; that operational requirement is a new preregistration condition and
does not alter v19.
