#!/bin/bash
# Save the BytePlus ModelArk API key to ~/.bash_profile without echoing it.
set -euo pipefail

profile="$HOME/.bash_profile"

read -rsp "Paste ARK API key, then press Enter (hidden): " key
echo
if [ -z "$key" ]; then
  echo "No key entered. Nothing changed."
  exit 1
fi

touch "$profile"
# Drop any earlier ARK_API_KEY line so there is only one.
grep -v '^export ARK_API_KEY=' "$profile" > "$profile.tmp" || true
mv "$profile.tmp" "$profile"
printf 'export ARK_API_KEY=%q\n' "$key" >> "$profile"
chmod 600 "$profile"

echo "Saved to $profile (${#key} characters). Open a new terminal tab to use it."
