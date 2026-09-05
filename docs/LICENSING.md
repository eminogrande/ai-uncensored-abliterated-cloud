# Licensing scope

## Our work: MIT

At the owner's request, the project-owned code, documentation and website in this
release are licensed under [MIT](../LICENSE), including our archived implementation.
The root Python/Node metadata and website notice must agree with that license.
Git history at the cleanup baseline lists Emin Mahrt as the commit author; no other
author's work is silently relicensed by this change.

## Why Apache-2.0 was there

The previous root `LICENSE` and Python package metadata selected Apache-2.0.
There is no recorded technical requirement for that choice. Using Vast.ai, Modal,
llama.cpp or an Apache-licensed model does not by itself require this project's own
code and documentation to use Apache-2.0.

This is a prospective license change by the owner, not a rewrite of history.
Earlier published releases remain available under their original Apache-2.0 terms;
that grant is not revoked. The original license text is retained in
[archive/licenses/Apache-2.0.txt](../archive/licenses/Apache-2.0.txt).

## What MIT does not change

- Downloaded model weights, tokenizers, model templates and projectors retain the
  licenses and notices of their exact upstream artifacts. We do not distribute model
  weights or claim ownership of them.
- Dependencies and third-party code keep their own license metadata and required
  notices. Dependency lockfile entries must not be globally rewritten to MIT.
- Article quotations, third-party artwork and other attributed materials retain their
  respective rights. MIT covers our original site code and prose, not every linked item.

Historical articles' model-license statements describe the named model, not the site
license. Keep that distinction visible rather than replacing every occurrence of
"Apache" with "MIT".
