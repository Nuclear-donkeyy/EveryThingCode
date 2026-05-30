const log = (label) => console.log(label);

async function loadProfile() {
  log("async:before await");
  const profile = await Promise.resolve({ name: "Ada", role: "admin" });
  log(`async:after await -> ${profile.name}/${profile.role}`);
}

log("script:start");

setTimeout(() => {
  log("timeout:task");
}, 0);

Promise.resolve()
  .then(() => log("promise:microtask 1"))
  .then(() => log("promise:microtask 2"));

queueMicrotask(() => {
  log("queueMicrotask:microtask");
});

loadProfile();

log("script:end");
