#!/usr/bin/env node
/**
 * Extract Mermaid blocks from docs/*.html and render to SVG (Persian-safe).
 * Output: docs/diagrams/{slug}-{index}.svg
 */
import { execFileSync } from 'node:child_process';
import { mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const DOCS = join(ROOT, 'docs');
const DIAGRAMS = join(DOCS, 'diagrams');
const MERMAID_RE = /<pre class="mermaid">\s*([\s\S]*?)<\/pre>/g;

function slugify(name) {
  return name.replace(/\.html$/i, '').replace(/[^\w\u0600-\u06FF-]+/g, '-').replace(/-+/g, '-');
}

function mmdcBin() {
  return join(DOCS, 'node_modules', '.bin', 'mmdc');
}

mkdirSync(DIAGRAMS, { recursive: true });

const htmlFiles = readdirSync(DOCS).filter(
  (f) => f.endsWith('.html') && !f.startsWith('_')
);

let total = 0;
const manifest = {};

for (const file of htmlFiles) {
  const content = readFileSync(join(DOCS, file), 'utf8');
  const slug = slugify(file);
  const diagrams = [];
  let match;
  let idx = 0;
  MERMAID_RE.lastIndex = 0;

  while ((match = MERMAID_RE.exec(content)) !== null) {
    const mmdPath = join(DIAGRAMS, `${slug}-${idx}.mmd`);
    const svgPath = join(DIAGRAMS, `${slug}-${idx}.svg`);
    const mermaidSource = match[1].trim();
    writeFileSync(mmdPath, mermaidSource, 'utf8');

    console.log(`Rendering ${slug}-${idx}.svg …`);
    execFileSync(
      mmdcBin(),
      ['-i', mmdPath, '-o', svgPath, '-b', 'white', '-t', 'neutral', '--scale', '2'],
      { stdio: 'inherit', cwd: DOCS }
    );

    diagrams.push(`diagrams/${slug}-${idx}.svg`);
    idx += 1;
    total += 1;
  }

  if (diagrams.length === 0) {
    console.log(`No diagrams in ${file}`);
  }
  manifest[file] = diagrams;
}

writeFileSync(
  join(DIAGRAMS, 'manifest.json'),
  JSON.stringify(manifest, null, 2),
  'utf8'
);

console.log(`Done: ${total} diagram(s) → docs/diagrams/`);
