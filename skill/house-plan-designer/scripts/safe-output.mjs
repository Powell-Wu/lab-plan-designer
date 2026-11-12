import fs from 'fs';
import path from 'path';

export function resetOutputDir(outArg) {
  if (!outArg) throw new Error('必须显式提供验收输出目录');
  const root = path.resolve(process.env.HOUSE_DESIGNER_WORK_ROOT || process.cwd());
  const out = path.resolve(outArg);
  const rel = path.relative(root, out);
  if (!rel || rel === '..' || rel.startsWith('..' + path.sep) || path.isAbsolute(rel)) {
    throw new Error(`拒绝清空目录：${out}。输出必须位于 ${root} 内，且不能等于工作根目录；可设置 HOUSE_DESIGNER_WORK_ROOT。`);
  }
  fs.rmSync(out, { recursive: true, force: true });
  fs.mkdirSync(out, { recursive: true });
  return out;
}
