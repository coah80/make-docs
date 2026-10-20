# Screenshots

A screenshot earns its place where the reader could go wrong: a choice screen, a hard-to-find button, the expected result, a destructive confirmation, or a screen that looks alarming but is normal. Capture each one from the real thing, so every label in the steps matches what the reader will see.

## Steps

1. **List the shots.** Walk the draft and mark each step that shows one of the screens above. Do this before capturing, so the capture run follows the doc in order.
2. **Pick a capture rig** for each surface:

   | Surface | Rig |
   |---|---|
   | Website or web app | Playwright, using a 1280-px-wide viewport |
   | Linux desktop app | a container with Xvfb, driven by `xdotool` and captured by `import` or `scrot` |
   | OS installer, boot menu, firmware screen | a VM (for example the `qemux/qemu` Docker image, with VNC driven by `vncdotool`). Pick UEFI and, if the doc covers it, Secure Boot. |
   | Windows app | the user's Windows machine, only when the user has given you access to it |
   | Phone, console, physical hardware | ask the user for photos, or the official docs' images with credit |

   For screens that last only seconds (countdowns, boot prompts), run a watcher that captures every second, so the screen is caught.
3. **Capture with safe inputs.** Use a throwaway disk, account and file each time. Use a test identity such as `Alex Player`, never the user's own. A tool that lists drives can show the host's real disks: cancel before any write, and use the screen only as a picture.
4. **Edit each image:**
   - Crop to the window or region the step is about. Remove the taskbar, desktop and other windows.
   - Blur anything personal or live: QR codes, email addresses, serial numbers, tokens, real usernames.
   - Save as PNG under one image folder, with names by page and screen (`install-destination.png`).
5. **Sync the text to the pictures.** Copy every label, message and example value from the captures into the steps. When the reader's screen will differ (a drive name, a logo), say so under the step: "In these pictures it is `QEMU HARDDISK 51.5 GB`. Yours shows your drive's brand and size."
6. **Place each image** right after its step, indented under the list item so the numbering keeps going. Write the alt text as what the reader should see, naming the control the step uses.
7. **Record the gaps.** A screen you could not capture gets a step written from the official docs and no picture. List it in your reply. A plausible mock-up misleads the reader, so leave the picture out.
8. **Clean up.** Delete VMs, disk images, downloaded installers, temporary accounts and scheduled tasks, on every machine you used.

You're done when every marked step has a real picture or a listed gap, every label in the text matches its picture, and nothing personal is visible.

## On the site

- Wide screenshots shrink to the content column. On a site you build, add click-to-zoom (`medium-zoom` on VitePress, initialised in the theme's `setup()` and on route change). Then add "Click any picture to see it full size." to the landing page.
- GitHub renders images at full width and opens them on click, so README images need no zoom.
