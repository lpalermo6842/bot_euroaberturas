<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DIPA ERP — Panel de Control</title>
    <!-- Tailwind CSS desde CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Íconos de Google Material Symbols -->
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
    <style>
        .material-symbols-outlined { font-size: 18px; }
    </style>
</head>
<body class="bg-[#F9FAFB] text-gray-800 font-sans text-sm h-screen flex overflow-hidden">

    <!-- 1. SIDEBAR IZQUIERDO -->
    <aside class="w-64 border-r border-gray-200 bg-white flex flex-col justify-between h-full flex-shrink-0">
        <div class="overflow-y-auto px-4 py-3">
            <!-- Logo -->
            <div class="flex items-center gap-2 mb-6 px-2">
                <span class="text-2xl font-black tracking-tight text-black">
                    D<span class="text-[#E50914]">I</span>PA
                </span>
            </div>

            <!-- Navegación -->
            <nav class="space-y-4">
                <div>
                    <p class="px-2 text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">Principal</p>
                    <ul class="space-y-0.5">
                        <li><a href="#" onclick="cambiarVista('inicio')" class="nav-btn flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">dashboard</span> Inicio</a></li>
                        <li><a href="#" onclick="cambiarVista('bandeja')" id="btn-bandeja" class="nav-btn flex items-center gap-2.5 px-2 py-1.5 rounded-md bg-red-50 text-[#E50914] font-medium"><span class="material-symbols-outlined">inbox</span> Bandeja de Entrada</a></li>
                        <li><a href="#" onclick="cambiarVista('staff')" class="nav-btn flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">admin_panel_settings</span> Bandeja de Staff</a></li>
                        <li><a href="#" onclick="cambiarVista('clientes')" class="nav-btn flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">group</span> Clientes</a></li>
                    </ul>
                </div>

                <div>
                    <p class="px-2 text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">Operación</p>
                    <ul class="space-y-0.5">
                        <li><a href="#" onclick="cambiarVista('agentes')" class="nav-btn flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">manage_accounts</span> Agentes</a></li>
                        <li><a href="#" onclick="cambiarVista('canales')" id="btn-canales" class="nav-btn flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">settings_input_antenna</span> Control de Canales</a></li>
                    </ul>
                </div>
            </nav>
        </div>

        <!-- Footer Sidebar -->
        <div class="p-3 border-t border-gray-200 bg-white space-y-3">
            <button class="w-full bg-[#E50914] hover:bg-red-700 text-white font-medium py-2 rounded-lg flex items-center justify-center gap-2 shadow-sm transition">
                <span class="material-symbols-outlined">add</span> Nuevo Mensaje
            </button>
            <div class="flex items-center justify-between pt-1">
                <div class="flex items-center gap-2">
                    <div class="w-8 h-8 rounded-full bg-gray-200 text-gray-700 font-bold flex items-center justify-center text-xs">AD</div>
                    <div>
                        <p class="font-semibold text-xs leading-none">Admin</p>
                        <p class="text-[10px] text-gray-400">admin</p>
                    </div>
                </div>
                <a href="logout.php" class="text-gray-400 hover:text-gray-600"><span class="material-symbols-outlined">logout</span></a>
            </div>
        </div>
    </aside>

    <!-- 2. ÁREA PRINCIPAL -->
    <div class="flex-1 flex flex-col h-full overflow-hidden">
        
        <!-- Header Superior -->
        <header class="h-14 border-b border-gray-200 bg-white px-6 flex items-center justify-between flex-shrink-0">
            <h1 id="titulo-pagina" class="text-lg font-bold text-gray-900">Bandeja de Entrada</h1>
            
            <div class="relative w-96">
                <span class="material-symbols-outlined absolute left-3 top-2.5 text-gray-400">search</span>
                <input type="text" placeholder="Buscar conversaciones, clientes..." class="w-full bg-gray-100 border-none rounded-lg pl-9 pr-4 py-1.5 text-xs focus:ring-2 focus:ring-red-500 focus:outline-none" />
            </div>

            <div class="flex items-center gap-4">
                <button class="text-gray-500 hover:text-gray-700"><span class="material-symbols-outlined">sensors</span></button>
                <button class="text-gray-500 hover:text-gray-700 relative">
                    <span class="material-symbols-outlined">notifications</span>
                    <span class="absolute -top-1 -right-1 w-2 h-2 bg-red-500 rounded-full"></span>
                </button>
                <div class="flex items-center gap-1.5 bg-gray-100 px-2.5 py-1 rounded-full text-xs font-medium text-gray-700">
                    <span class="w-2 h-2 rounded-full bg-emerald-500"></span> En línea
                </div>
                <div class="w-7 h-7 rounded-full bg-gray-200 text-gray-700 font-bold flex items-center justify-center text-xs">AD</div>
            </div>
        </header>

        <!-- CONTENEDOR DINÁMICO (Cambia con JS) -->
        <main id="contenido-dinamico" class="flex-1 overflow-y-auto">
            
            <!-- VISTA: BANDEJA DE ENTRADA (Por defecto) -->
            <div id="vista-bandeja" class="flex h-full overflow-hidden">
                <div class="w-[420px] border-r border-gray-200 bg-white flex flex-col h-full flex-shrink-0">
                    <div class="p-4 border-b border-gray-100 space-y-3">
                        <div class="flex gap-1 overflow-x-auto pb-1 text-xs">
                            <button class="px-3 py-1 rounded-full bg-blue-100 text-blue-700 font-medium">Nuevos</button>
                            <button class="px-3 py-1 rounded-full bg-gray-100 text-gray-600">Progreso</button>
                            <button class="px-3 py-1 rounded-full bg-gray-100 text-gray-600">Espera</button>
                            <button class="px-3 py-1 rounded-full bg-gray-100 text-gray-600">Cerrados 15</button>
                        </div>
                        <input type="text" placeholder="Nombre, número o mensaje..." class="w-full border border-gray-200 rounded-lg px-3 py-1.5 text-xs focus:ring-1 focus:ring-red-500 focus:outline-none" />
                    </div>
                    <div class="flex-1 flex flex-col items-center justify-center p-6 text-center text-gray-400">
                        <span class="material-symbols-outlined text-3xl mb-2">inbox</span>
                        <p class="font-semibold text-gray-700 text-sm">Sin conversaciones</p>
                    </div>
                </div>
                <div class="flex-1 bg-[#F9FAFB] flex flex-col items-center justify-center p-8 text-center">
                    <span class="material-symbols-outlined text-4xl text-[#E50914] mb-3">chat_bubble_outline</span>
                    <h2 class="text-base font-bold text-gray-800">Selecciona una conversación</h2>
                    <p class="text-xs text-gray-500 mt-1">Elige un chat de la lista para comenzar a responder.</p>
                </div>
            </div>

            <!-- VISTA: CONTROL DE CANALES (Oculta al inicio) -->
            <div id="vista-canales" class="hidden p-6 space-y-6">
                <!-- Métricas superioles -->
                <div class="flex items-center justify-between">
                    <div>
                        <h2 class="text-xl font-bold text-gray-900">📡 Centro de Control de Canales</h2>
                        <p class="text-xs text-gray-500">Configurá cómo responde el CRM en cada punto de contacto: bot, IA, horarios y más.</p>
                    </div>
                    <button class="bg-[#E50914] text-white px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5">
                        <span class="material-symbols-outlined">bar_chart</span> Consumos Meta
                    </button>
                </div>

                <!-- KPIs -->
                <div class="grid grid-cols-3 gap-4">
                    <div class="bg-white p-4 rounded-xl border border-gray-200 text-center">
                        <span class="text-2xl font-bold text-gray-900">3</span>
                        <p class="text-xs text-gray-400">Canales Totales</p>
                    </div>
                    <div class="bg-white p-4 rounded-xl border border-gray-200 text-center">
                        <span class="text-2xl font-bold text-emerald-600">2</span>
                        <p class="text-xs text-gray-400">Activos</p>
                    </div>
                    <div class="bg-white p-4 rounded-xl border border-gray-200 text-center">
                        <span class="text-2xl font-bold text-red-500">2</span>
                        <p class="text-xs text-gray-400">Configurados</p>
                    </div>
                </div>

                <!-- Cards de Canales -->
                <div class="grid grid-cols-3 gap-4">
                    <!-- Telegram Card -->
                    <div class="bg-white border border-gray-200 rounded-xl p-4 flex flex-col justify-between space-y-4">
                        <div class="flex justify-between items-start">
                            <div class="flex items-center gap-2">
                                <span class="material-symbols-outlined text-blue-500 text-2xl">send</span>
                                <div>
                                    <h3 class="font-bold text-sm">telegram</h3>
                                    <span class="text-[10px] text-gray-400 uppercase font-semibold">TELEGRAM</span>
                                </div>
                            </div>
                            <span class="bg-emerald-50 text-emerald-600 px-2 py-0.5 rounded-full text-[10px] font-bold">● ACTIVO</span>
                        </div>
                        <div class="text-xs space-y-1.5 text-gray-600">
                            <div class="flex justify-between"><span>Modo:</span> <span class="font-semibold text-gray-800">⚡ IA Híbrida</span></div>
                            <div class="flex justify-between"><span>Horario:</span> <span class="text-gray-800">🌐 Global</span></div>
                            <div class="flex justify-between"><span>Derivación:</span> <span class="text-gray-800">🔄 Cola general</span></div>
                        </div>
                        <button class="w-full bg-[#E50914] text-white py-1.5 rounded-lg text-xs font-medium hover:bg-red-700 transition">✏️ Editar Configuración</button>
                    </div>

                    <!-- WhatsApp Card -->
                    <div class="bg-white border border-gray-200 rounded-xl p-4 flex flex-col justify-between space-y-4">
                        <div class="flex justify-between items-start">
                            <div class="flex items-center gap-2">
                                <span class="material-symbols-outlined text-emerald-500 text-2xl">chat</span>
                                <div>
                                    <h3 class="font-bold text-sm">Dipa Distribucion</h3>
                                    <span class="text-[10px] text-gray-400 uppercase font-semibold">WHATSAPP</span>
                                </div>
                            </div>
                            <span class="bg-emerald-50 text-emerald-600 px-2 py-0.5 rounded-full text-[10px] font-bold">● ACTIVO</span>
                        </div>
                        <div class="text-xs space-y-1.5 text-gray-600">
                            <div class="flex justify-between"><span>Modo:</span> <span class="font-semibold text-gray-800">⚡ IA Híbrida</span></div>
                            <div class="flex justify-between"><span>Horario:</span> <span class="text-gray-800">⏰ Personalizado</span></div>
                            <div class="flex justify-between"><span>Derivación:</span> <span class="text-gray-800">🔄 Cola general</span></div>
                        </div>
                        <button class="w-full bg-[#E50914] text-white py-1.5 rounded-lg text-xs font-medium hover:bg-red-700 transition">✏️ Editar Configuración</button>
                    </div>

                    <!-- Chat Web Card -->
                    <div class="bg-white border border-gray-200 rounded-xl p-4 flex flex-col justify-between space-y-4">
                        <div class="flex justify-between items-start">
                            <div class="flex items-center gap-2">
                                <span class="material-symbols-outlined text-indigo-500 text-2xl">language</span>
                                <div>
                                    <h3 class="font-bold text-sm">Chat Cliente Web</h3>
                                    <span class="text-[10px] text-gray-400 uppercase font-semibold">CHAT PÚBLICO</span>
                                </div>
                            </div>
                            <span class="bg-pink-50 text-pink-600 px-2 py-0.5 rounded-full text-[10px] font-bold">SIEMPRE ACTIVO</span>
                        </div>
                        <div class="text-xs space-y-1.5 text-gray-600">
                            <div class="flex justify-between"><span>Modo:</span> <span class="font-semibold text-gray-400">⚙️ Sin configurar</span></div>
                            <div class="flex justify-between"><span>Identificación:</span> <span class="text-gray-800">👤 Anónimo</span></div>
                            <div class="flex justify-between"><span>URL pública:</span> <span class="text-blue-600 underline">/chat-cliente ↗</span></div>
                        </div>
                        <button class="w-full border border-gray-300 text-gray-700 py-1.5 rounded-lg text-xs font-medium hover:bg-gray-50 transition">⚙️ Configurar Canal</button>
                    </div>
                </div>
            </div>

        </main>
    </div>

    <!-- SCRIPT DE NAVEGACIÓN DINÁMICA -->
    <script>
        function cambiarVista(vista) {
            const vistaBandeja = document.getElementById('vista-bandeja');
            const vistaCanales = document.getElementById('vista-canales');
            const titulo = document.getElementById('titulo-pagina');

            // Reset de estilos de menú
            document.querySelectorAll('.nav-btn').forEach(btn => {
                btn.classList.remove('bg-red-50', 'text-[#E50914]', 'font-medium');
                btn.classList.add('text-gray-600');
            });

            if (vista === 'canales') {
                vistaBandeja.classList.add('hidden');
                vistaCanales.classList.remove('hidden');
                titulo.innerText = 'Centro de Control de Canales';
                document.getElementById('btn-canales').classList.add('bg-red-50', 'text-[#E50914]', 'font-medium');
            } else if (vista === 'bandeja') {
                vistaCanales.classList.add('hidden');
                vistaBandeja.classList.remove('hidden');
                titulo.innerText = 'Bandeja de Entrada';
                document.getElementById('btn-bandeja').classList.add('bg-red-50', 'text-[#E50914]', 'font-medium');
            }
        }
    </script>
</body>
</html>