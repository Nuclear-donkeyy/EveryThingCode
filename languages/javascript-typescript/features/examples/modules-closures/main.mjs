function createCounter(name, start = 0) {
  let count = start;
  const history = [];

  return {
    increment(step = 1) {
      count += step;
      history.push({ action: "increment", step, value: count });
      return count;
    },
    snapshot() {
      return {
        name,
        count,
        history: history.map((entry) => ({ ...entry })),
      };
    },
  };
}

const pageViews = createCounter("page-views");
const retries = createCounter("retries", 2);

pageViews.increment();
pageViews.increment(4);
retries.increment();

console.log("pageViews", pageViews.snapshot());
console.log("retries", retries.snapshot());
console.log("direct count access", pageViews.count);
