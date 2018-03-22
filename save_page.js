const fs = require("fs");
const path = require("path");
const spawn = require("child_process").spawn;
const uuid = require("node-uuid");

const pdfExecutable = "phantomjs";

function makeOutFileName(url) {
  const fileName = url
    .replace("http://", "")
    .replace("https://", "")
    .replace(".", "-dot-")
    .replace("/", "-");
  return path.join(__dirname, "out", "js", `${fileName}-${uuid.v4()}.pdf`);
}

function generatePdf(url) {
  const paperFormat = "A4";
  const orientation = "portrait";
  const margin = "1cm";
  zoom = "1";
  const tmpFile = makeOutFileName(url);

  const options = [
    "--web-security=no",
    "--ssl-protocol=any",
    path.join(__dirname, "rasterize.js"),
    url,
    tmpFile,
    paperFormat,
    orientation,
    margin,
    zoom
  ];

  const pdfProcess = spawn(pdfExecutable, options);
  pdfProcess.stdout.on("data", function(data) {
    console.log("pdf: " + data);
  });
  pdfProcess.stderr.on("data", function(data) {
    console.error("pdf: " + data);
  });
  pdfProcess.on("close", function(code) {
    if (code) {
      return next(new Error("Wrong code: " + code));
    }
  });
}

generatePdf("http://peterfonseca.gq");
