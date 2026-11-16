// Configuración pública de la app. La llave "anon" de Supabase es pública por diseño:
// las tablas están cerradas y solo se accede mediante funciones que exigen la clave personal.
window.PLAZA_CONFIG = {
  supabaseUrl: "https://zydxazpkuaevzkkxmhnb.supabase.co",
  supabaseKey: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp5ZHhhenBrdWFldnpra3htaG5iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTQ0ODg3NDcsImV4cCI6MjExMDA2NDc0N30.XeIUWoM14X2EXC-hd7o5VtGYzg-pV-4Vy5KN4xW2bwo",
  // Cada cargo tiene su propio marco (componentes y familias), índice de lotes y plan de lectura.
  // Los lotes se comparten: un ítem aparece en un cargo solo si su familia está en el marco de ese cargo.
  cargos: {
    docente_ti: { nombre: "Docente de aula · Tecnología e Informática", datos: "data/", meta: 60 },
    coordinador: { nombre: "Directivo docente · Coordinador", datos: "data/coord/", meta: 70 }
  },
  preguntasPorReto: 10,
  maxRepasoPorReto: 4,
  vidas: 5,
  simulacroPreguntas: 30,
  minutosPorPregunta: 3,
  horaSimulacro: "08:00",
  vapidPublic: "BJsHJbs-oKq4i26aQNEJvVe5IKLRxNhsLHD5_UMyRD81bT05EwqqM0Wr-TqXoiWgukYeGcFy08Xg-rC5jfUK42w",
  pushUrl: "https://zydxazpkuaevzkkxmhnb.supabase.co/functions/v1/recordatorios"
};
