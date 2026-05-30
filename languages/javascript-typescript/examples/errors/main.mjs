async function loadName(ok) {
  if (!ok) throw new Error("config missing");
  return "learner";
}

try {
  console.log(await loadName(false));
} catch (error) {
  console.log(`recover: ${error.message}`);
}
