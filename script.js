// Alterna tema
function alternarTema() { 
  document.body.classList.toggle("light"); 
  localStorage.setItem("tema", document.body.classList.contains("light") ? "claro" : "escuro");
}

// Bloqueio de inspeção (estético)
document.addEventListener("contextmenu", e => e.preventDefault());
document.addEventListener("keydown", e => {
  if (e.key === "F12" || 
      (e.ctrlKey && e.shiftKey && ["i","j","c"].includes(e.key.toLowerCase())) || 
      (e.ctrlKey && e.key.toLowerCase() === "u")) e.preventDefault();
});

// Logo flutuante
const logo = document.getElementById("logo");
const floatingLogo = document.getElementById("logo-floating");
logo.addEventListener("mouseenter", () => floatingLogo.style.opacity = "1");
logo.addEventListener("mouseleave", () => floatingLogo.style.opacity = "0");
logo.addEventListener("mousemove", e => {
  floatingLogo.style.left = `${e.clientX}px`;
  floatingLogo.style.top = `${e.clientY}px`;
});

// Mantém tema salvo
if(localStorage.getItem("tema") === "claro") document.body.classList.add("light");
