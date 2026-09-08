const writeAbilities = new Set([
  "novamira/gutenberg-add-pending-change",
  "novamira/gutenberg-enable-batch-finalization",
  "novamira/gutenberg-write-content",
  "novamira/execute-php",
  "novamira/write-file",
  "novamira/edit-file",
  "novamira/delete-file"
]);

export function assertAllowed(client, ability, parameters = {}) {
  if (Array.isArray(client.allowedAbilities) && !client.allowedAbilities.includes(ability)) {
    throw new Error(`A habilidade ${ability} não está autorizada para ${client.id}`);
  }
  if (writeAbilities.has(ability) && parameters.confirm !== true) {
    throw new Error(`A operação ${ability} exige confirm=true`);
  }
}
