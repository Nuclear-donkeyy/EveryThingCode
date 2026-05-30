class ConfigLoadError extends Error {
  constructor(part, cause) {
    super(`could not load ${part}`, { cause });
    this.name = "ConfigLoadError";
    this.code = "E_CONFIG_LOAD";
    this.part = part;
  }
}

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function loadConfigPart(part) {
  await wait(part.delay);

  if (part.fail) {
    throw new ConfigLoadError(part.name, new Error(part.reason));
  }

  return [part.name, part.value];
}

async function loadAllConfig(parts) {
  const settled = await Promise.allSettled(parts.map(loadConfigPart));
  const config = {};
  const errors = [];

  for (const result of settled) {
    if (result.status === "fulfilled") {
      const [name, value] = result.value;
      config[name] = value;
      console.log("loaded", name, value);
    } else {
      errors.push(result.reason);
      console.log("failed", result.reason.part, result.reason.code);
      console.log("cause:", result.reason.cause.message);
    }
  }

  return { config, errors };
}

async function main() {
  const parts = [
    { name: "featureFlags", delay: 10, value: { checkoutV2: true } },
    { name: "secrets", delay: 20, fail: true, reason: "vault timeout" },
    { name: "limits", delay: 5, value: { maxBatchSize: 100 } },
  ];

  const { config, errors } = await loadAllConfig(parts);
  console.log("usable config", config);

  if (errors.length > 0) {
    throw new Error(`startup blocked by ${errors.length} config error(s)`, {
      cause: errors[0],
    });
  }
}

main().catch((error) => {
  console.log("startup blocked", error.message);
  console.log("first cause", error.cause.message);
});
