// Disable right-click
document.addEventListener("contextmenu", (e) => e.preventDefault());
// Disable devtools shortcuts
document.addEventListener("keydown", (e) => {
  // F12
  if (e.key === "F12") {
    e.preventDefault();
    return;
  }

  // Ctrl + Shift + I / J / C
  if (
    e.ctrlKey &&
    e.shiftKey &&
    ["I", "J", "C"].includes(e.key.toUpperCase())
  ) {
    e.preventDefault();
    return;
  }

  // Ctrl + U
  if (e.ctrlKey && e.key.toUpperCase() === "U") {
    e.preventDefault();
    return;
  }
});
