const unidecode = require("unidecode");

let sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
let clean = (data) => {
  let data_cleaned = data;
  if (typeof data == "string") {
    data_cleaned = data
      .replace("\n", "")
      .replace("\r", "")
      .replace("\t", "")
      .trim();
    data_cleaned = unidecode(data_cleaned);
    return data_cleaned;
  }
  if (Array.isArray(data)) {
    let filtered = data.filter(function (el) {
      return el.trim() != "";
    });
    data_cleaned = filtered.map((e) => clean(e));
    return data_cleaned;
  }
};

module.exports = { sleep, clean };
