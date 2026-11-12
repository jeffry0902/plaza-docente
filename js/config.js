// Configuración pública de la app. La llave "anon" de Supabase es pública por diseño:
// las tablas están cerradas y solo se accede mediante funciones que exigen la clave personal.
window.PLAZA_CONFIG = {
  supabaseUrl: "https://zydxazpkuaevzkkxmhnb.supabase.co",
  supabaseKey: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp5ZHhhenBrdWFldnpra3htaG5iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTQ0ODg3NDcsImV4cCI6MjExMDA2NDc0N30.XeIUWoM14X2EXC-hd7o5VtGYzg-pV-4Vy5KN4xW2bwo",
  marcoUrl: "data/marco.json",
  indiceUrl: "data/indice.json",
  preguntasPorReto: 10,
  maxRepasoPorReto: 4,
  vidas: 5,
  simulacroPreguntas: 30,
  minutosPorPregunta: 3,
  horaSimulacro: "08:00"
};
