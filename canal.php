<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bandeja de Entrada | DIPA ERP</title>
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
                        <li><a href="#" class="flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">dashboard</span> Inicio</a></li>
                        <li><a href="#" class="flex items-center gap-2.5 px-2 py-1.5 rounded-md bg-red-50 text-[#E50914] font-medium"><span class="material-symbols-outlined">inbox</span> Bandeja de Entrada</a></li>
                        <li><a href="#" class="flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">admin_panel_settings</span> Bandeja de Staff</a></li>
                        <li><a href="#" class="flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">group</span> Clientes</a></li>
                    </ul>
                </div>

                <div>
                    <p class="px-2 text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">Inteligencia IA & Gerencia</p>
                    <ul class="space-y-0.5">
                        <li><a href="#" class="flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">query_stats</span> Consola Manager <span class="text-[10px] font-semibold bg-gray-100 px-1.5 py-0.5 rounded text-gray-500">LIVE</span></a></li>
                        <li><a href="#" class="flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">auto_fix_high</span> Compositor IA</a></li>
                        <li><a href="#" class="flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">smart_toy</span> Automatizaciones</a></li>
                        <li><a href="#" class="flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">schema</span> Flujos Automáticos</a></li>
                        <li><a href="#" class="flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">psychology</span> Orquestación IA</a></li>
                        <li><a href="#" class="flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">account_tree</span> Flujo de Info y SLA</a></li>
                        <li><a href="#" class="flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">forum</span> Chatbot Clientes</a></li>
                        <li><a href="#" class="flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">campaign</span> Campañas</a></li>
                    </ul>
                </div>

                <div>
                    <p class="px-2 text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">Operación</p>
                    <ul class="space-y-0.5">
                        <li><a href="#" class="flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">manage_accounts</span> Agentes</a></li>
                        <li><a href="#" class="flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">support_agent</span> Preventistas</a></li>
                        <li><a href="#" class="flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">corporate_fare</span> Departamentos</a></li>
                        <li><a href="#" class="flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">bolt</span> Respuestas Rápidas</a></li>
                        <li><a href="#" class="flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">sell</span> Etiquetas</a></li>
                        <li><a href="#" class="flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">hub</span> Conexiones</a></li>
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
                    <div class="w-8 h-8 rounded-full bg-gray-200 text-gray-700 font-bold flex items-center justify-center text-xs">
                        AD
                    </div>
                    <div>
                        <p class="font-semibold text-xs leading-none">Admin</p>
                        <p class="text-[10px] text-gray-400">admin</p>
                    </div>
                </div>
                <a href="logout.php" class="text-gray-400 hover:text-gray-600">
                    <span class="material-symbols-outlined">logout</span>
                </a>
            </div>
        </div>
    </aside>

    <!-- 2. ÁREA PRINCIPAL -->
    <div class="flex-1 flex flex-col h-full overflow-hidden">
        
        <!-- Header Superior -->
        <header class="h-14 border-b border-gray-200 bg-white px-6 flex items-center justify-between flex-shrink-0">
            <h1 class="text-lg font-bold text-gray-900">Bandeja de Entrada</h1>
            
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
                    <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                    En línea
                </div>
                <div class="w-7 h-7 rounded-full bg-gray-200 text-gray-700 font-bold flex items-center justify-center text-xs">
                    AD
                </div>
            </div>
        </header>

        <!-- Cuerpo Principal (Split Screen) -->
        <div class="flex-1 flex overflow-hidden">
            
            <!-- Columna Izquierda: Filtros y Lista de Chats -->
            <div class="w-[420px] border-r border-gray-200 bg-white flex flex-col h-full flex-shrink-0">
                <div class="p-4 border-b border-gray-100 space-y-3">
                    
                    <!-- Status pills -->
                    <div class="flex gap-1 overflow-x-auto pb-1 text-xs" id="status-filters">
                        <button class="px-3 py-1 rounded-full bg-blue-100 text-blue-700 font-medium">Nuevos</button>
                        <button class="px-3 py-1 rounded-full bg-gray-100 text-gray-600 hover:bg-gray-200">Progreso</button>
                        <button class="px-3 py-1 rounded-full bg-gray-100 text-gray-600 hover:bg-gray-200">Espera</button>
                        <button class="px-3 py-1 rounded-full bg-gray-100 text-gray-600 hover:bg-gray-200">Cerrados 15</button>
                        <button class="px-3 py-1 rounded-full bg-gray-100 text-gray-600 hover:bg-gray-200">Alertas</button>
                    </div>

                    <!-- Canal pills -->
                    <div class="flex items-center gap-1 text-xs">
                        <button class="px-2.5 py-1 rounded-full border border-gray-400 bg-gray-50 font-medium">Todos</button>
                        <button class="px-2.5 py-1 rounded-full border border-transparent text-gray-500 hover:bg-gray-100 flex items-center gap-1">
                            <span class="w-2 h-2 rounded-full bg-emerald-500"></span> WA
                        </button>
                        <button class="px-2.5 py-1 rounded-full border border-transparent text-gray-500 hover:bg-gray-100 flex items-center gap-1">
                            <span class="w-2 h-2 rounded-full bg-blue-500"></span> FB
                        </button>
                        <button class="px-2.5 py-1 rounded-full border border-transparent text-gray-500 hover:bg-gray-100 flex items-center gap-1">
                            <span class="w-2 h-2 rounded-full bg-pink-500"></span> IG
                        </button>
                    </div>

                    <!-- Acordeón Guía -->
                    <div class="border border-gray-200 rounded-lg p-2.5 bg-gray-50 text-xs">
                        <details class="group">
                            <summary class="flex items-center justify-between font-medium text-gray-700 cursor-pointer list-none">
                                <div class="flex items-center gap-1.5">
                                    <span class="material-symbols-outlined">menu_book</span>
                                    <span>Guía de Uso: Bandeja de Chats</span>
                                </div>
                                <span class="material-symbols-outlined group-open:rotate-180 transition-transform">expand_more</span>
                            </summary>
                            <div class="mt-2 text-gray-500 text-[11px] space-y-1">
                                <p>• <strong>Cómo usarlo:</strong> Chatea en tiempo real con clientes.</p>
                                <p>• <strong>Origen:</strong> MySQL local + PostgreSQL Sigma ERP.</p>
                            </div>
                        </details>
                    </div>

                    <!-- Buscador e Insumos Ajax -->
                    <input type="text" id="chat-search" placeholder="Nombre, número o mensaje..." class="w-full border border-gray-200 rounded-lg px-3 py-1.5 text-xs focus:ring-1 focus:ring-red-500 focus:outline-none" />

                    <select id="depto-select" class="w-full border border-gray-200 rounded-lg px-3 py-1.5 text-xs text-gray-600 bg-white focus:outline-none">
                        <option value="">(Todos los departamentos)</option>
                        <option value="1">CONTACT CENTER</option>
                        <option value="2">CUENTAS CORRIENTES</option>
                        <option value="3">LOGISTICA</option>
                    </select>
                </div>

                <!-- Lista de Conversaciones (Dynamic via JS / AJAX) -->
                <div id="chats-container" class="flex-1 flex flex-col items-center justify-center p-6 text-center text-gray-400">
                    <div class="w-12 h-12 rounded-lg bg-gray-100 flex items-center justify-center mb-3">
                        <span class="material-symbols-outlined text-2xl text-gray-400">inbox</span>
                    </div>
                    <p class="font-semibold text-gray-700 text-sm">Sin conversaciones</p>
                    <p class="text-xs text-gray-400 mt-1">No hay conversaciones que coincidan con los filtros.</p>
                </div>

                <!-- Footer Lista -->
                <div class="p-3 border-t border-gray-200 flex items-center justify-between bg-white text-xs text-gray-500">
                    <span id="chat-count">0 conversaciones</span>
                    <div class="flex items-center gap-2">
                        <button class="flex items-center gap-1 border border-gray-200 px-2.5 py-1 rounded hover:bg-gray-50">
                            <span class="material-symbols-outlined">download</span> Exportar
                        </button>
                        <button class="flex items-center gap-1 border border-gray-200 px-2.5 py-1 rounded hover:bg-gray-50">
                            <span class="material-symbols-outlined">assignment_ind</span> Asignar
                        </button>
                    </div>
                </div>
            </div>

            <!-- Columna Derecha: Panel de Chat -->
            <div id="chat-view" class="flex-1 bg-[#F9FAFB] flex flex-col items-center justify-center p-8 text-center relative">
                <div class="w-14 h-14 rounded-2xl bg-red-100 text-[#E50914] flex items-center justify-center mb-4 shadow-sm">
                    <span class="material-symbols-outlined text-3xl">chat_bubble_outline</span>
                </div>
                <h2 class="text-base font-bold text-gray-800">Selecciona una conversación</h2>
                <p class="text-xs text-gray-500 mt-1 max-w-sm">
                    Elige una conversación de la lista para comenzar a responder mensajes en tiempo real.
                </p>
                <div class="mt-4 inline-flex items-center gap-1.5 bg-gray-200/60 px-2.5 py-1 rounded text-[11px] text-gray-600">
                    Atajo: <kbd class="bg-white px-1.5 py-0.5 rounded shadow-sm font-semibold text-gray-800">N</kbd> para nueva conversación
                </div>
            </div>

        </div>
    </div>

    <!-- Script para interacción AJAX con PHP -->
    <script>
        // Ejemplo de petición AJAX para traer los chats desde un endpoint PHP (ej. obtener_chats.php)
        function cargarChats() {
            const depto = document.getElementById('depto-select').value;
            const search = document.getElementById('chat-search').value;

            fetch(`obtener_chats.php?depto=${depto}&search=${search}`)
                .then(response => response.json())
                .then(data => {
                    // Lógica para actualizar el contenedor de chats
                    console.log("Chats cargados:", data);
                })
                .catch(error => console.error("Error cargando chats:", error));
        }

        document.getElementById('depto-select').addEventListener('change', cargarChats);
        document.getElementById('chat-search').addEventListener('input', cargarChats);
    </script>
</body>
</html>