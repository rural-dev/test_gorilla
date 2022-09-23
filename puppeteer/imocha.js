const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");
const createCsvWriter = require("csv-writer").createObjectCsvWriter;
const { clean, sleep } = require("./utils");

// Variables
let starting_url = "https://www.imocha.io/pre-employment-testing/all-tests";
let output_path = "./imocha_raw.csv";

(async () => {
  puppeteer.use(StealthPlugin());
  const browser = await puppeteer.launch({
    headless: false,
    args: ["--no-sandbox"],
  });
  const page = await browser.newPage();
  await page.setJavaScriptEnabled(true);
  await page.setDefaultNavigationTimeout(0);
  await page.goto(starting_url);
  const xpath_expression = '//ul[@id="allTestDiv"]/li/a[@href]';
  await page.waitForXPath(xpath_expression);
  const links = await page.$x(xpath_expression);
  const link_urls = await page.evaluate((...links) => {
    return links.map((e) => e.href);
  }, ...links);
  let result = [];
  const getDetail = async (link, retry) => {
    console.log(retry);
    if (retry == 0) {
      console.log(" retryNumber exceeded maxRetryNumber ! ");
      return false;
    }
    try {
      await page.goto(link);
      await page.waitForXPath("//h1");
      let [h1] = await page.$x("//h1");
      let title = await page.evaluate((h1) => h1.textContent, h1);
      let type2 = await page.$("div.test-detail-inner > ul > li > span");
      if (type2) {
        let topics = await page.$$eval(
          "body > header > div > div:nth-child(3) > div.col-md-8.col-lg-9 > div:nth-child(2) > ul.list-inline.tag-ul > li > span",
          (texts) => {
            return texts.map((text) => text.textContent);
          }
        );
        let [duration_el] = await page.$x(
          '//strong[contains(text(),"Test Duration:")]/parent::span'
        );
        let duration = await page.evaluate(
          (duration_el) => duration_el.textContent,
          duration_el
        );
        let [question_el] = await page.$x(
          '//strong[contains(text(),"No. of Questions:")]//parent::span'
        );
        let question = await page.evaluate(
          (question_el) => question_el.textContent,
          question_el
        );
        result.push({
          url: link,
          title: clean(title),
          candidate: "",
          organization: "",
          description: "",
          summary: "",
          hiring: "",
          topics: clean(topics).join("\n"),
          duration: clean(duration),
          question: clean(question),
          level: "",
        });
      } else {
        let [can_el] = await page.$x(
          '//p[contains(text(),"Candidates Assessed")]/following-sibling::h6[1]'
        );
        let candidate = await page.evaluate(
          (can_el) => can_el.textContent,
          can_el
        );
        let [org_el] = await page.$x(
          '//p[contains(text(),"Organisations Served")]/following-sibling::h6[1]'
        );
        let organization = await page.evaluate(
          (org_el) => org_el.textContent,
          org_el
        );
        let description = await page.$$eval(
          "div.test-detail-inner > p",
          (texts) => {
            return texts.map((text) => text.textContent);
          }
        );

        let summary = await page.$$eval(
          "body > section.pt-4.color-darkblue > div > div > div.col-md-8.list-right-arrow-small > p",
          (texts) => {
            return texts.map((text) => text.textContent);
          }
        );

        let hiring = await page.$$eval(
          "body > section.pt-4.color-darkblue > div > div > div.col-md-3.align-self-lg-center > ul > li",
          (texts) => {
            return texts.map((text) => text.textContent);
          }
        );
        let topics = [];

        if (
          await page.$(
            "body > section:nth-child(11) > div > div:nth-child(2) > div > div > div:nth-child(2) > h6"
          )
        ) {
          topics = await page.$$eval(
            "body > section:nth-child(11) > div > div:nth-child(2) > div",
            (divs) => {
              return divs.map((div) => {
                let divText = "";
                if (div.querySelector("div > div:nth-child(2) > h6")) {
                  divText = div.querySelector(
                    "div > div:nth-child(2) > h6"
                  ).innerText;
                }
                let divDesc = "";
                if (div.querySelector("div > div:nth-child(2) > p")) {
                  divDesc = div.querySelector(
                    "div > div:nth-child(2) > p"
                  ).innerText;
                }
                return `${divText}: ${divDesc}`;
              });
            }
          );
        }
        let [duration_el] = await page.$x(
          '//b[contains(text(),"Test Duration:")]/span'
        );
        let duration = await page.evaluate(
          (duration_el) => duration_el.textContent,
          duration_el
        );
        let [question_el] = await page.$x(
          '//b[contains(text(),"No. of Questions:")]/span'
        );
        let question = await page.evaluate(
          (question_el) => question_el.textContent,
          question_el
        );
        let [level_el] = await page.$x(
          '//b[contains(text(),"Level of Expertise:")]/span'
        );
        let level = await page.evaluate(
          (level_el) => level_el.textContent,
          level_el
        );
        result.push({
          url: link,
          title: clean(title),
          candidate: clean(candidate),
          organization: clean(organization),
          description: clean(description).join("\n"),
          summary: clean(summary).join("\n"),
          hiring: clean(hiring).join("\n"),
          topics: clean(topics).join("\n"),
          duration: clean(duration),
          question: clean(question),
          level: clean(level),
        });
      }
    } catch (e) {
      console.log(e);
      await sleep(3000);
      await getDetail(link, retry - 1);
    }
  };
  for (let i = 0; i < link_urls.length; i++) {
    await getDetail(link_urls[i], 3);
  }
  const csvWriter = createCsvWriter({
    header: [
      { id: "url", title: "url" },
      { id: "title", title: "title" },
      { id: "candidate", title: "candidate" },
      { id: "organization", title: "organization" },
      { id: "description", title: "description" },
      { id: "summary", title: "summary" },
      { id: "hiring", title: "hiring" },
      { id: "topics", title: "topics" },
      { id: "duration", title: "duration" },
      { id: "question", title: "question" },
      { id: "level", title: "level" },
    ],
    path: output_path,
  });
  csvWriter.writeRecords(result).then(() => {
    console.log("...Done");
  });
  console.log(result);
  await browser.close();
})();
