# developer-vault
all content for developers

- [architect](plugins/architect/README.md): arquitectura, decisiones y diseño.
- [developer](plugins/developer/README.md): implementación y consulta sobre código.
- [reviewer](plugins/reviewer/README.md): entender una PR y construir la review junto con la persona.

## Shared decisions and specialist guidance

Architect and developer share an approval protocol: new design and business
choices are presented to the user before implementation; previous approvals
remain valid. The coordinating agent verifies the handoff and consolidates open
questions. Local implementation details remain autonomous within the approved
scope. Review consultations remain read-only.

Each plugin packages selected guidance from the other as private, generated
references, so installation of the other plugin is optional. The maintained
sources remain with their owning skill. See the plugin READMEs for maintenance
and `evals/shared-design-v1/summary.md` for verification evidence and limits.
