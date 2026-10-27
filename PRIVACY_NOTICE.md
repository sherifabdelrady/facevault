# Privacy Notice — FaceVault

FaceVault is provided as a research prototype for face recognition and
liveness detection. Before deploying in any production or real-world context:

1. **Consent:** Collect explicit, informed consent from all individuals
   whose face embeddings are stored or processed.
2. **Data minimisation:** Store embeddings only as long as necessary.
   Do not store raw face images alongside embeddings unless required.
3. **Access control:** Restrict embedding storage to authorised services only.
   Implement authentication on all API endpoints.
4. **Intended use:** This system is NOT validated for high-stakes decisions
   (employment, law enforcement, access control) without appropriate evaluation.
5. **Anti-spoofing:** The liveness detection component is an architecture sketch
   and has NOT been evaluated on any presentation-attack dataset.
   Do not rely on it for security-critical deployments.
6. **Regulatory compliance:** Depending on your jurisdiction, face recognition
   systems may require specific legal authorisation (GDPR Art. 9, BIPA, etc.).
