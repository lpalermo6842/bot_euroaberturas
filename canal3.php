<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DIPA ERP — Panel Unificado</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Google Material Symbols -->
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
    <style>
        .material-symbols-outlined { font-size: 18px; }
    </style>
</head>
<body class="bg-[#F9FAFB] text-gray-800 font-sans text-sm h-screen flex overflow-hidden">

    <!-- 1. SIDEBAR IZQUIERDO -->
    <aside class="w-64 border-r border-gray-200 bg-white flex flex-col justify-between h-full flex-shrink-0">
        <div class="overflow-y-auto px-4 py-3">
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
                        <li><a href="#" onclick="cambiarVista('bandeja')" id="btn-bandeja" class="nav-btn flex items-center gap-2.5 px-2 py-1.5 rounded-md bg-red-50 text-[#E50914] font-medium"><span class="material-symbols-outlined">inbox</span> Bandeja de Entrada</a></li>
                    </ul>
                </div>

                <div>
                    <p class="px-2 text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">Inteligencia IA & Gerencia</p>
                    <ul class="space-y-0.5">
                        <li><a href="#" onclick="cambiarVista('flujos')" id="btn-flujos" class="nav-btn flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">schema</span> Flujos Automáticos</a></li>
                    </ul>
                </div>

                <div>
                    <p class="px-2 text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">Operación</p>
                    <ul class="space-y-0.5">
                        <li><a href="#" onclick="cambiarVista('departamentos')" id="btn-departamentos" class="nav-btn flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">corporate_fare</span> Departamentos</a></li>
                        <li><a href="#" onclick="cambiarVista('respuestas')" id="btn-respuestas" class="nav-btn flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">bolt</span> Respuestas Rápidas</a></li>
                        <li><a href="#" onclick="cambiarVista('etiquetas')" id="btn-etiquetas" class="nav-btn flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">sell</span> Etiquetas</a></li>
                        <li><a href="#" onclick="cambiarVista('conexiones')" id="btn-conexiones" class="nav-btn flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">hub</span> Conexiones</a></li>
                        <li><a href="#" onclick="cambiarVista('canales')" id="btn-canales" class="nav-btn flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">settings_input_antenna</span> Control de Canales</a></li>
                        <li><a href="#" onclick="cambiarVista('consumos')" id="btn-consumos" class="nav-btn flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">monitoring</span> Consumos Meta</a></li>
                    </ul>
                </div>

                <div>
                    <p class="px-2 text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">Herramientas</p>
                    <ul class="space-y-0.5">
                        <li><a href="#" onclick="cambiarVista('webhooks')" id="btn-webhooks" class="nav-btn flex items-center gap-2.5 px-2 py-1.5 rounded-md text-gray-600 hover:bg-gray-100"><span class="material-symbols-outlined">anchor</span> Webhooks (Logs)</a></li>
                    </ul>
                </div>
            </nav>
        </div>

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
                <a href="#" class="text-gray-400 hover:text-gray-600"><span class="material-symbols-outlined">logout</span></a>
            </div>
        </div>
    </aside>

    <!-- 2. ÁREA PRINCIPAL -->
    <div class="flex-1 flex flex-col h-full overflow-hidden">
        
        <!-- Header -->
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

        <!-- VISTAS DINÁMICAS -->
        <main id="contenido-dinamico" class="flex-1 overflow-y-auto">

            <!-- VISTA 1: BANDEJA DE ENTRADA -->
            <div id="vista-bandeja" class="vista-seccion flex h-full overflow-hidden">
                <div class="w-[420px] border-r border-gray-200 bg-white flex flex-col h-full flex-shrink-0">
                    <div class="p-4 border-b border-gray-100 space-y-3">
                        <div class="flex gap-1 overflow-x-auto pb-1 text-xs">
                            <button class="px-3 py-1 rounded-full bg-blue-100 text-blue-700 font-medium">Nuevos</button>
                            <button class="px-3 py-1 rounded-full bg-gray-100 text-gray-600">Progreso</button>
                            <button class="px-3 py-1 rounded-full bg-gray-100 text-gray-600">Espera</button>
                            <button class="px-3 py-1 rounded-full bg-gray-100 text-gray-600">Cerrados 15</button>
                        </div>
                        <input type="text" placeholder="Nombre, número o mensaje..." class="w-full border border-gray-200 rounded-lg px-3 py-1.5 text-xs focus:ring-1 focus:ring-red-500 focus:outline-none" />
                        <select class="w-full border border-gray-200 rounded-lg px-3 py-1.5 text-xs text-gray-600 bg-white">
                            <option>(Todos los departamentos)</option>
                            <option>CONTACT CENTER</option>
                            <option>CUENTAS CORRIENTES</option>
                        </select>
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

            <!-- VISTA 2: FLUJOS AUTOMÁTICOS -->
            <div id="vista-flujos" class="vista-seccion hidden p-6 space-y-6">
                <div class="flex justify-between items-center">
                    <div>
                        <h2 class="text-xl font-bold">Automatización de Flujos</h2>
                        <p class="text-xs text-gray-500">Configura disparadores en segundo plano, plazos de inactividad y respuestas automáticas.</p>
                    </div>
                    <button class="bg-[#E50914] text-white px-3 py-1.5 rounded-lg text-xs font-medium">+ Nueva Automatización</button>
                </div>
                <div class="space-y-4">
                    <div class="bg-white border p-4 rounded-xl space-y-3">
                        <div class="flex justify-between items-center"><h3 class="font-bold text-sm">⌛ Espera Prolongada</h3><input type="checkbox" checked /></div>
                        <div class="grid grid-cols-2 gap-4">
                            <div><label class="text-xs text-gray-500">Tiempo de disparo (minutos)</label><input type="number" value="10" class="w-full border p-1.5 rounded text-xs mt-1" /></div>
                            <div><label class="text-xs text-gray-500">Mensaje de Alerta</label><textarea class="w-full border p-1.5 rounded text-xs mt-1">Hola, seguimos aquí...</textarea></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- VISTA 3: DEPARTAMENTOS -->
            <div id="vista-departamentos" class="vista-seccion hidden p-6 space-y-4">
                <div class="flex justify-between items-center">
                    <div><h2 class="text-xl font-bold">Departamentos / Colas</h2><p class="text-xs text-gray-500">Organiza colas de atención y equipos.</p></div>
                    <button class="bg-[#E50914] text-white px-3 py-1.5 rounded-lg text-xs font-medium">+ Nuevo Departamento</button>
                </div>
                <div class="bg-white border rounded-xl overflow-hidden">
                    <table class="w-full text-left text-xs">
                        <thead class="bg-gray-50 border-b">
                            <tr><th class="p-3">Nombre</th><th class="p-3">Código</th><th class="p-3">Estado</th><th class="p-3">Agentes</th><th class="p-3">Acciones</th></tr>
                        </thead>
                        <tbody>
                            <tr class="border-b"><td class="p-3 font-bold">CONTACT CENTER</td><td class="p-3 text-gray-500">contact-center</td><td class="p-3"><span class="bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded-full font-bold">ACTIVO</span></td><td class="p-3">👤 3</td><td class="p-3">✏️ 🚫 🗑️</td></tr>
                            <tr class="border-b"><td class="p-3 font-bold">CUENTAS CORRIENTES</td><td class="p-3 text-gray-500">cuentas-corrientes</td><td class="p-3"><span class="bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded-full font-bold">ACTIVO</span></td><td class="p-3">👤 1</td><td class="p-3">✏️ 🚫 🗑️</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- VISTA 4: RESPUESTAS RÁPIDAS -->
            <div id="vista-respuestas" class="vista-seccion hidden p-6 space-y-4">
                <div class="flex justify-between items-center">
                    <div><h2 class="text-xl font-bold">Respuestas Rápidas</h2><p class="text-xs text-gray-500">Atajos de teclado para agentes (/hola).</p></div>
                    <button class="bg-[#E50914] text-white px-3 py-1.5 rounded-lg text-xs font-medium">+ Nueva Respuesta</button>
                </div>
                <div class="grid grid-cols-3 gap-4">
                    <div class="bg-white border p-4 rounded-xl space-y-2">
                        <div class="flex justify-between"><span class="bg-red-50 text-[#E50914] font-bold px-2 py-0.5 rounded text-xs">/ALTA</span><div>✏️ 🗑️</div></div>
                        <p class="text-xs text-gray-600">Proceso de alta de cliente comercial DIPA ERP.</p>
                    </div>
                </div>
            </div>

            <!-- VISTA 5: ETIQUETAS -->
            <div id="vista-etiquetas" class="vista-seccion hidden p-6 space-y-4">
                <div class="flex justify-between items-center">
                    <div><h2 class="text-xl font-bold">Administración de Etiquetas</h2><p class="text-xs text-gray-500">Etiquetas visuales para conversaciones.</p></div>
                    <button class="bg-[#E50914] text-white px-3 py-1.5 rounded-lg text-xs font-medium">+ Nueva Etiqueta</button>
                </div>
                <div class="bg-white border rounded-xl overflow-hidden">
                    <table class="w-full text-left text-xs">
                        <thead class="bg-gray-50 border-b"><tr><th class="p-3">Nombre</th><th class="p-3">Color</th><th class="p-3">Tipo</th><th class="p-3">Acciones</th></tr></thead>
                        <tbody>
                            <tr class="border-b"><td class="p-3 font-bold">AGENTE</td><td class="p-3"><span class="inline-block w-3 h-3 rounded-full bg-red-600 mr-1"></span>#ca0b0f</td><td class="p-3"><span class="bg-blue-50 text-blue-600 px-2 py-0.5 rounded">AUTO (IA)</span></td><td class="p-3">✏️ 🗑️</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- VISTA 6: CONEXIONES -->
            <div id="vista-conexiones" class="vista-seccion hidden p-6 space-y-4">
                <div class="flex justify-between items-center">
                    <div><h2 class="text-xl font-bold">Conexiones de Canales</h2><p class="text-xs text-gray-500">Integraciones WABA Meta, Telegram, etc.</p></div>
                    <button class="bg-[#E50914] text-white px-3 py-1.5 rounded-lg text-xs font-medium">+ Nueva Conexión</button>
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div class="bg-white border p-4 rounded-xl space-y-2">
                        <div class="flex justify-between items-center"><h3 class="font-bold">Dipa Distribución</h3><span class="bg-emerald-50 text-emerald-600 px-2 py-0.5 rounded text-[10px] font-bold">● ACTIVO</span></div>
                        <p class="text-xs text-gray-500">Proveedor: Meta Cloud API (1113722021832336)</p>
                    </div>
                </div>
            </div>

            <!-- VISTA 7: CONTROL DE CANALES -->
            <div id="vista-canales" class="vista-seccion hidden p-6 space-y-6">
                <div><h2 class="text-xl font-bold">📡 Centro de Control de Canales</h2><p class="text-xs text-gray-500">Configura respuestas, bot, IA y derivación por canal.</p></div>
                <div class="grid grid-cols-3 gap-4">
                    <div class="bg-white border p-4 rounded-xl"><span class="text-2xl font-bold">3</span><p class="text-xs text-gray-400">Canales Totales</p></div>
                    <div class="bg-white border p-4 rounded-xl"><span class="text-2xl font-bold text-emerald-600">2</span><p class="text-xs text-gray-400">Activos</p></div>
                    <div class="bg-white border p-4 rounded-xl"><span class="text-2xl font-bold text-red-500">2</span><p class="text-xs text-gray-400">Configurados</p></div>
                </div>
            </div>

            <!-- VISTA 8: CONSUMOS META -->
            <div id="vista-consumos" class="vista-seccion hidden p-6 space-y-6">
                <div><h2 class="text-xl font-bold">📊 Consumos de Meta API</h2><p class="text-xs text-gray-500">Monitoreo de conversaciones y costos estimados.</p></div>
                <div class="grid grid-cols-4 gap-4">
                    <div class="bg-white border p-4 rounded-xl"><span class="text-2xl font-bold">44</span><p class="text-xs text-gray-400">Enviados</p></div>
                    <div class="bg-white border p-4 rounded-xl"><span class="text-2xl font-bold">42</span><p class="text-xs text-gray-400">Recibidos</p></div>
                    <div class="bg-white border p-4 rounded-xl"><span class="text-2xl font-bold">50%</span><p class="text-xs text-gray-400">Tasa Lectura</p></div>
                    <div class="bg-white border p-4 rounded-xl"><span class="text-2xl font-bold text-emerald-600">$1.19 USD</span><p class="text-xs text-gray-400">Costo Estimado</p></div>
                </div>
            </div>

            <!-- VISTA 9: WEBHOOK LOGS -->
            <div id="vista-webhooks" class="vista-seccion hidden p-6 space-y-4">
                <div><h2 class="text-xl font-bold">Eventos Webhook (Logs)</h2><p class="text-xs text-gray-500">Consola de auditoría de respuestas API en tiempo real.</p></div>
                <div class="bg-white border rounded-xl overflow-hidden">
                    <table class="w-full text-left text-xs">
                        <thead class="bg-gray-50 border-b"><tr><th class="p-3">Fecha/Hora</th><th class="p-3">Canal</th><th class="p-3">Sentido</th><th class="p-3">Estado</th><th class="p-3">Payload</th></tr></thead>
                        <tbody>
                            <tr class="border-b"><td class="p-3 text-gray-500">2026-08-27 17:45</td><td class="p-3 font-bold text-pink-600">WHATSAPP</td><td class="p-3"><span class="bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded">ENTRADA</span></td><td class="p-3"><span class="bg-blue-100 text-blue-700 px-2 py-0.5 rounded">OK</span></td><td class="p-3 font-mono text-gray-400">{"object":"whatsapp_business..."}</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>

        </main>
    </div>

    <!-- NAVEGACIÓN Y LÓGICA DINÁMICA -->
    <script>
        const vistas = {
            'bandeja': { id: 'vista-bandeja', btn: 'btn-bandeja', titulo: 'Bandeja de Entrada' },
            'flujos': { id: 'vista-flujos', btn: 'btn-flujos', titulo: 'Automatización de Flujos' },
            'departamentos': { id: 'vista-departamentos', btn: 'btn-departamentos', titulo: 'Departamentos / Colas' },
            'respuestas': { id: 'vista-respuestas', btn: 'btn-respuestas', titulo: 'Respuestas Rápidas' },
            'etiquetas': { id: 'vista-etiquetas', btn: 'btn-etiquetas', titulo: 'Administración de Etiquetas' },
            'conexiones': { id: 'vista-conexiones', btn: 'btn-conexiones', titulo: 'Conexiones de Canales' },
            'canales': { id: 'vista-canales', btn: 'btn-canales', titulo: 'Centro de Control de Canales' },
            'consumos': { id: 'vista-consumos', btn: 'btn-consumos', titulo: 'Consumos de Meta API (WhatsApp)' },
            'webhooks': { id: 'vista-webhooks', btn: 'btn-webhooks', titulo: 'Eventos Webhook (Logs)' }
        };

        function cambiarVista(clave) {
            // Ocultar todas las vistas
            document.querySelectorAll('.vista-seccion').forEach(el => el.classList.add('hidden'));
            
            // Reset de estilos en el menú
            document.querySelectorAll('.nav-btn').forEach(btn => {
                btn.classList.remove('bg-red-50', 'text-[#E50914]', 'font-medium');
                btn.classList.add('text-gray-600');
            });

            // Activar la vista elegida
            const vista = vistas[clave];
            if (vista) {
                document.getElementById(vista.id).classList.remove('hidden');
                document.getElementById(vista.btn).classList.add('bg-red-50', 'text-[#E50914]', 'font-medium');
                document.getElementById('titulo-pagina').innerText = vista.titulo;
            }
        }
    </script>
</body>
</html>