import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { launch } from './skill/house-plan-designer/scripts/browser.mjs';

const R = path.dirname(fileURLToPath(import.meta.url));
const browser = await launch({ headless: true, gpu: false, viewport: { width: 1600, height: 1050 } });
const page = await browser.newPage();
const errors = [];
page.on('pageerror', e => errors.push(String(e)));
try {
  await page.goto(pathToFileURL(path.join(R, 'residential-demo.html')).href + '?debug', { waitUntil: 'load' });
  await page.waitForFunction(() => window.__designer, { timeout: 30000 });
  const floors = [];
  for (let i = 0; i < 2; i++) {
    floors.push(await page.evaluate(fi => {
      const D = window.__designer;
      D.goFloor(fi);
      const P = D.app.plan;
      return {
        floor: fi,
        name: P.name,
        rooms: P.rooms.length,
        furniture: P.furniture.length,
        electricalPoints: P.elec.length,
        mepKeys: P.mep ? Object.keys(P.mep) : [],
        customRuns: P.mep?.custom?.length || 0,
        issues: D.runChecks().issues,
      };
    }, i));
  }
  const checks = {
    twoFloors: floors.length === 2,
    furnished: floors.every(f => f.furniture >= 20),
    electrified: floors.every(f => f.electricalPoints >= 10),
    noModelErrors: floors.every(f => !f.issues.some(i => i.level === 'error')),
    noPageErrors: errors.length === 0,
  };
  const report = { pass: Object.values(checks).every(Boolean), checks, floors, errors, screenshotsGenerated: 0 };
  const output = process.env.VERIFICATION_OUTPUT ? path.resolve(process.env.VERIFICATION_OUTPUT) : path.join(R, 'verification.json');
  fs.writeFileSync(output, JSON.stringify(report, null, 2));
  console.log(JSON.stringify({ pass: report.pass, checks, floors: floors.map(f => ({ name: f.name, rooms: f.rooms, furniture: f.furniture, electricalPoints: f.electricalPoints, errors: f.issues.filter(i => i.level === 'error').length, warnings: f.issues.filter(i => i.level === 'warn').map(i => i.msg), info: f.issues.filter(i => i.level === 'info').length })), errors, screenshotsGenerated: 0 }, null, 2));
  if (!report.pass) process.exitCode = 1;
} finally {
  await browser.close();
}
