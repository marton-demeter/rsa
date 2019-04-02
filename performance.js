const { exec } = require('child_process');
const { writeFileSync, existsSync } = require('fs');

let ks = [2048, 4096];
const TEST_NUM = 100;
const FNAME = 'data.json';

let ctr = 0;
let idx = -1;

let results = {}
try { results = require(`./${FNAME}`) } catch(e) {}

save_file = () => {
  writeFileSync(FNAME, JSON.stringify(results,null,2));
}

process.on('exit', save_file);

process.on('SIGINT', () => process.exit(1));

loop = () => {
  if(ctr % TEST_NUM == 0) {
    ctr = 0;
    idx++;
  }
  if(idx == ks.length) {
    save_file()
    process.exit(0)
  }
  proc = exec(`python3 genkeys.py test ${ks[idx]}`, (err, stdout, stderr) => {
    console.log(ks[idx],ctr, stdout.split('in')[1].split(' ')[1]);
    if(results[ks[idx]])
      results[ks[idx]].push(stdout.split('in')[1].split(' ')[1]);
    else
      results[ks[idx]] = [stdout.split('in')[1].split(' ')[1]];
    loop(ctr++);
  });
}

loop(ctr);

