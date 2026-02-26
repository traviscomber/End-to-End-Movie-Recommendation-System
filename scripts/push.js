const { execSync } = require('child_process');

try {
  console.log('[v0] Adding all changes...');
  execSync('git add -A', { stdio: 'inherit' });
  
  console.log('[v0] Committing changes...');
  execSync('git commit -m "Fix: Remove invalid runtime config from vercel.json"', { stdio: 'inherit' });
  
  console.log('[v0] Pushing to GitHub...');
  execSync('git push origin project-development', { stdio: 'inherit' });
  
  console.log('[v0] ✓ Changes pushed successfully!');
  console.log('[v0] Vercel deployment should start automatically...');
} catch (error) {
  console.error('[v0] Error:', error.message);
  process.exit(1);
}
