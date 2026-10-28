-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 28-10-2026 a las 20:21:04
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `sistema_soporte_ia`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `incidencias`
--

CREATE TABLE `incidencias` (
  `id` int(11) NOT NULL,
  `codigo_ticket` varchar(50) NOT NULL,
  `fecha_registro` datetime DEFAULT current_timestamp(),
  `descripcion_texto` text NOT NULL,
  `categoria_sugerida` enum('Hardware','Software','Redes','Accesos','Impresoras') DEFAULT NULL,
  `prioridad_sugerida` enum('Baja','Media','Alta','Crítica') DEFAULT NULL,
  `tiempo_procesamiento_ia` float DEFAULT 0,
  `categoria_final` enum('Hardware','Software','Redes','Accesos','Impresoras') DEFAULT NULL,
  `prioridad_final` enum('Baja','Media','Alta','Crítica') DEFAULT NULL,
  `estado` enum('Pendiente','Validado','Cerrado') DEFAULT 'Pendiente',
  `usuario_id` int(11) DEFAULT NULL,
  `fecha_actualizacion` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `incidencias`
--

INSERT INTO `incidencias` (`id`, `codigo_ticket`, `fecha_registro`, `descripcion_texto`, `categoria_sugerida`, `prioridad_sugerida`, `tiempo_procesamiento_ia`, `categoria_final`, `prioridad_final`, `estado`, `usuario_id`, `fecha_actualizacion`) VALUES
(1, 'TICK-3318', '2026-10-20 12:43:21', 'La impresora no tiene mucha tinta, no me permite imprimir ', 'Hardware', 'Alta', 0.0027, 'Impresoras', 'Alta', 'Validado', NULL, '2026-10-24 01:13:56'),
(2, 'TICK-6834', '2026-10-23 11:28:17', 'Mi archivo word no se pudo guardar correctamente, deseo recuperarlo', 'Hardware', 'Media', 0.0044, 'Software', 'Media', 'Validado', NULL, '2026-10-23 16:51:08'),
(3, 'TICK-4508', '2026-10-23 19:54:20', 'El programa Excel no abre, me sale licencia vencida', 'Hardware', 'Media', 0.004, 'Software', 'Baja', 'Validado', NULL, '2026-10-24 00:58:45'),
(4, 'TICK-7595', '2026-10-23 20:05:00', 'La impresora se atasco, no deja sacar el papel ', 'Impresoras', 'Baja', 0.0022, 'Impresoras', 'Media', 'Validado', NULL, '2026-10-24 01:14:05'),
(5, 'TICK-6072', '2026-10-23 21:51:09', 'No puedo acceder a la pagina de google, me sale que no tengo conexión a internet', 'Hardware', 'Alta', 0.0043, 'Redes', 'Alta', 'Validado', NULL, '2026-10-24 02:52:52'),
(6, 'TICK-2651', '2026-10-24 11:43:22', 'La computadora de escritorio no enciende ni emite luces en el panel frontal.', 'Hardware', 'Alta', 0.0032, 'Hardware', 'Crítica', 'Validado', NULL, '2026-10-24 16:56:12'),
(7, 'TICK-7557', '2026-10-24 11:43:37', 'El sistema operativo Windows lanza una pantalla azul constante al abrir Microsoft Excel.', 'Software', 'Media', 0.002, 'Software', 'Alta', 'Validado', NULL, '2026-10-24 16:55:54'),
(8, 'TICK-1595', '2026-10-24 11:43:50', 'No hay conexión a internet ni acceso a los recursos de la red corporativa en todo el piso.', 'Hardware', 'Media', 0.002, 'Redes', 'Crítica', 'Validado', NULL, '2026-10-24 16:55:44'),
(9, 'TICK-2340', '2026-10-24 11:43:59', 'Olvidé mi contraseña de acceso al dominio y el sistema bloqueó mi cuenta de usuario.', 'Accesos', 'Alta', 0.003, 'Accesos', 'Alta', 'Validado', NULL, '2026-10-24 16:55:29'),
(10, 'TICK-6616', '2026-10-24 11:44:10', 'La impresora multifuncional de la oficina principal tiene un atasco severo de papel.', 'Impresoras', 'Baja', 0.002, 'Impresoras', 'Media', 'Validado', NULL, '2026-10-24 16:55:00'),
(11, 'TICK-4331', '2026-10-24 11:44:16', 'El monitor parpadea constantemente y pierde la señal de video de forma intermitente.', 'Hardware', 'Media', 0.0019, 'Hardware', 'Baja', 'Validado', NULL, '2026-10-24 16:53:30'),
(12, 'TICK-6757', '2026-10-24 11:44:25', 'El software de gestión interna se congela al momento de exportar los reportes diarios.', 'Software', 'Media', 0.002, 'Software', 'Alta', 'Validado', NULL, '2026-10-24 16:53:11'),
(13, 'TICK-6392', '2026-10-24 11:44:34', 'La velocidad de la red Wi-Fi es muy lenta para realizar las llamadas con los clientes.', 'Redes', 'Media', 0.002, 'Redes', 'Media', 'Validado', NULL, '2026-10-24 16:52:58'),
(14, 'TICK-2536', '2026-10-24 11:44:43', 'Necesito solicitar permisos temporales para instalar una aplicación aprobada por TI.', 'Hardware', 'Media', 0.002, 'Accesos', 'Baja', 'Validado', NULL, '2026-10-24 16:52:30'),
(15, 'TICK-8799', '2026-10-24 11:44:51', 'La impresora láser no reconoce el cartucho de tóner nuevo y parpadea en rojo.', 'Hardware', 'Baja', 0.002, 'Impresoras', 'Alta', 'Validado', NULL, '2026-10-24 16:52:17'),
(16, 'TICK-2826', '2026-10-24 11:58:02', 'El disco duro principal de la laptop está haciendo un zumbido extraño y el sistema se congela por completo.', 'Hardware', 'Media', 0.002, 'Hardware', 'Crítica', 'Validado', NULL, '2026-10-24 17:04:50'),
(17, 'TICK-1115', '2026-10-24 11:58:12', 'Tras la última actualización de Windows, las macros del sistema de contabilidad dejaron de funcionar.', 'Hardware', 'Alta', 0.002, 'Software', 'Alta', 'Validado', NULL, '2026-10-24 17:04:32'),
(18, 'TICK-4537', '2026-10-24 11:58:29', 'No hay conexión al servidor central de archivos ni acceso a las carpetas compartidas del área.', 'Accesos', 'Alta', 0.002, 'Redes', 'Crítica', 'Validado', NULL, '2026-10-24 17:04:20'),
(19, 'TICK-3276', '2026-10-24 11:58:43', 'El usuario no puede iniciar sesión en el portal corporativo porque su cuenta está bloqueada por intentos fallidos.', 'Hardware', 'Media', 0.001, 'Accesos', 'Media', 'Validado', NULL, '2026-10-24 17:03:38'),
(20, 'TICK-1582', '2026-10-24 11:58:53', 'La impresora de la oficina está imprimiendo las hojas con líneas blancas verticales muy marcadas.', 'Impresoras', 'Baja', 0.003, 'Impresoras', 'Baja', 'Validado', NULL, '2026-10-24 17:03:13'),
(21, 'TICK-9667', '2026-10-24 11:59:04', 'Varias teclas del teclado integrado (letras y símbolos) no responden al momento de escribir.', 'Hardware', 'Media', 0.003, 'Hardware', 'Media', 'Validado', NULL, '2026-10-24 17:02:57'),
(22, 'TICK-3636', '2026-10-24 11:59:12', 'El navegador web se cierra inesperadamente cada vez que intento ingresar a la plataforma de llamadas.', 'Hardware', 'Media', 0.0019, 'Software', 'Baja', 'Validado', NULL, '2026-10-24 17:02:29'),
(23, 'TICK-6543', '2026-10-24 11:59:20', 'Hay intermitencia severa en la red inalámbrica de la oficina de ventas, impidiendo atender pedidos.', 'Hardware', 'Alta', 0.002, 'Redes', 'Alta', 'Validado', NULL, '2026-10-24 17:02:07'),
(24, 'TICK-3379', '2026-10-24 11:59:37', 'Se requiere el alta y provisión de credenciales de acceso al sistema para un nuevo colaborador de operaciones.', 'Accesos', 'Media', 0.001, 'Accesos', 'Baja', 'Validado', NULL, '2026-10-24 17:01:57'),
(25, 'TICK-3194', '2026-10-24 11:59:46', 'La impresora de recepción se encuentra sin tóner y parpadea con luz roja fija sin dejar imprimir.', 'Impresoras', 'Baja', 0.002, 'Impresoras', 'Alta', 'Validado', NULL, '2026-10-24 17:01:35'),
(26, 'TICK-9735', '2026-10-24 12:17:41', 'El adaptador de corriente de la laptop no transmite energía y la batería ha llegado al 0%.', 'Hardware', 'Alta', 0.002, 'Hardware', 'Alta', 'Validado', NULL, '2026-10-24 17:24:23'),
(27, 'TICK-2591', '2026-10-24 12:18:01', 'La licencia del software de ofimática ha expirado y no permite guardar cambios en los documentos.', 'Hardware', 'Alta', 0.002, 'Software', 'Media', 'Validado', NULL, '2026-10-24 17:24:17'),
(28, 'TICK-5086', '2026-10-24 12:18:18', 'Se ha caído la red local y no hay conexión Ethernet en todo el pabellón de operaciones.', 'Hardware', 'Media', 0.004, 'Redes', 'Crítica', 'Validado', NULL, '2026-10-24 17:23:40'),
(29, 'TICK-1771', '2026-10-24 12:18:26', 'El sistema rechaza las credenciales de acceso al dominio corporativo a pesar de ser correctas.', 'Accesos', 'Media', 0.001, 'Accesos', 'Media', 'Validado', NULL, '2026-10-24 17:23:23'),
(30, 'TICK-8041', '2026-10-24 12:18:36', 'La impresora departamental indica error de tóner agotado a pesar de haber instalado uno nuevo.', 'Impresoras', 'Baja', 0.002, 'Impresoras', 'Baja', 'Validado', NULL, '2026-10-24 17:23:12'),
(31, 'TICK-9752', '2026-10-24 12:18:43', 'Los puertos USB del equipo no detectan ningún tipo de memoria flash ni periférico conectado.', 'Hardware', 'Alta', 0.002, 'Hardware', 'Baja', 'Validado', NULL, '2026-10-24 17:22:59'),
(32, 'TICK-1041', '2026-10-24 12:18:52', 'El navegador muestra un error crítico de certificado al intentar abrir el portal de la compañía.', 'Software', 'Media', 0.001, 'Software', 'Media', 'Validado', NULL, '2026-10-24 17:22:25'),
(33, 'TICK-1706', '2026-10-24 12:19:00', 'La conexión VPN se desconecta de manera intermitente cada vez que intento enviar archivos pesados.', 'Hardware', 'Alta', 0.002, 'Redes', 'Alta', 'Validado', NULL, '2026-10-24 17:22:10'),
(34, 'TICK-4662', '2026-10-24 12:19:12', 'Solicitud de restablecimiento urgente de contraseña para el sistema de atención al cliente.', 'Accesos', 'Media', 0.003, 'Accesos', 'Alta', 'Validado', NULL, '2026-10-24 17:22:02'),
(35, 'TICK-3862', '2026-10-24 12:19:21', 'La impresora multifuncional no procesa las solicitudes de escaneo y se queda congelada.', 'Impresoras', 'Baja', 0.001, 'Impresoras', 'Media', 'Validado', NULL, '2026-10-24 17:21:55'),
(36, 'TICK-9289', '2026-10-24 12:25:24', 'La pantalla táctil del equipo portátil no responde al tacto en ninguna zona.', 'Hardware', 'Alta', 0.001, 'Hardware', 'Alta', 'Validado', NULL, '2026-10-24 17:32:09'),
(37, 'TICK-4565', '2026-10-24 12:25:41', 'El sistema de facturación electrónica arroja un error crítico de base de datos al generar comprobantes.', 'Software', 'Media', 0.001, 'Software', 'Crítica', 'Validado', NULL, '2026-10-24 17:31:32'),
(38, 'TICK-5108', '2026-10-24 12:25:53', 'La señal de Wi-Fi se corta constantemente en el área de recepción de las oficinas.', 'Hardware', 'Media', 0.002, 'Redes', 'Media', 'Validado', NULL, '2026-10-24 17:31:16'),
(39, 'TICK-2291', '2026-10-24 12:26:09', 'El usuario no recuerda su contraseña temporal para el sistema de soporte y necesita un reseteo.', 'Hardware', 'Media', 0.002, 'Accesos', 'Baja', 'Validado', NULL, '2026-10-24 17:28:53'),
(40, 'TICK-9022', '2026-10-24 12:26:18', 'La impresora de etiquetas no alinea correctamente el texto en las cintas de código de barras.', 'Hardware', 'Baja', 0.002, 'Impresoras', 'Media', 'Validado', NULL, '2026-10-24 17:28:41'),
(41, 'TICK-4164', '2026-10-24 12:26:28', 'El ventilador del procesador suena con demasiada fuerza y la computadora se calienta muy rápido.', 'Hardware', 'Media', 0.001, 'Hardware', 'Alta', 'Validado', NULL, '2026-10-24 17:28:09'),
(42, 'TICK-5242', '2026-10-24 12:26:36', 'Microsoft Outlook no sincroniza los correos entrantes ni permite enviar mensajes nuevos.', 'Hardware', 'Alta', 0.001, 'Software', 'Alta', 'Validado', NULL, '2026-10-24 17:27:56'),
(43, 'TICK-6666', '2026-10-24 12:26:43', 'Hay un corte total de comunicación con la sucursal remota por caída de la línea dedicada.', 'Hardware', 'Alta', 0.002, 'Redes', 'Crítica', 'Validado', NULL, '2026-10-24 17:27:44'),
(44, 'TICK-8000', '2026-10-24 12:26:51', 'Se necesita revocar los permisos de acceso al servidor de recursos humanos para un ex colaborador.', 'Accesos', 'Alta', 0.001, 'Accesos', 'Alta', 'Validado', NULL, '2026-10-24 17:27:26'),
(45, 'TICK-1572', '2026-10-24 12:27:00', 'La impresora multifuncional muestra el mensaje de bandeja de papel vacía a pesar de estar llena.', 'Impresoras', 'Baja', 0.001, 'Impresoras', 'Baja', 'Validado', NULL, '2026-10-24 17:27:22'),
(46, 'TICK-2354', '2026-10-24 12:34:12', 'La bandeja del lector de CD/DVD no abre al presionar el botón físico del equipo.', 'Hardware', 'Media', 0.003, 'Hardware', 'Baja', 'Validado', NULL, '2026-10-24 17:43:39'),
(47, 'TICK-1279', '2026-10-24 12:34:22', 'El antivirus corporativo bloquea un software legítimo de diseño interno impidiendo trabajar.', 'Hardware', 'Media', 0.002, 'Software', 'Alta', 'Validado', NULL, '2026-10-24 17:44:04'),
(48, 'TICK-1189', '2026-10-24 12:34:32', 'Corte total de fibra óptica afectando la conectividad de internet en toda la sede principal.', 'Hardware', 'Alta', 0.001, 'Redes', 'Crítica', 'Validado', NULL, '2026-10-24 17:43:52'),
(49, 'TICK-8713', '2026-10-24 12:34:47', 'Solicitud de cambio de nombre de usuario y correo corporativo por actualización de datos.', 'Hardware', 'Media', 0.001, 'Accesos', 'Media', 'Validado', NULL, '2026-10-24 17:43:03'),
(50, 'TICK-9359', '2026-10-24 12:34:59', 'La impresora de contabilidad tiene configurado el tamaño de papel incorrecto de forma predeterminada.', 'Impresoras', 'Baja', 0.001, 'Impresoras', 'Baja', 'Validado', NULL, '2026-10-24 17:42:47'),
(51, 'TICK-6205', '2026-10-24 12:35:07', 'La fuente de poder del servidor principal emite un olor a quemado y se apaga de forma imprevista.', 'Hardware', 'Alta', 0.001, 'Hardware', 'Crítica', 'Validado', NULL, '2026-10-24 17:42:32'),
(52, 'TICK-1831', '2026-10-24 12:35:18', 'El navegador web se congela por completo al intentar abrir múltiples pestañas corporativas.', 'Software', 'Media', 0.002, 'Software', 'Media', 'Validado', NULL, '2026-10-24 17:42:22'),
(53, 'TICK-2520', '2026-10-24 12:35:24', 'La red VPN se desconecta automáticamente cada diez minutos para todos los usuarios remotos.', 'Hardware', 'Media', 0.002, 'Redes', 'Alta', 'Validado', NULL, '2026-10-24 17:42:01'),
(54, 'TICK-9658', '2026-10-24 12:35:43', 'Un excolaborador desvinculado aún mantiene acceso activo a los directorios del sistema financiero.', 'Accesos', 'Alta', 0.002, 'Accesos', 'Crítica', 'Validado', NULL, '2026-10-24 17:41:31'),
(55, 'TICK-8974', '2026-10-24 12:35:55', 'La impresora láser de gerencia no toma las hojas de la bandeja de alimentación manual.', 'Impresoras', 'Baja', 0.002, 'Impresoras', 'Alta', 'Validado', NULL, '2026-10-24 17:41:20'),
(56, 'TICK-6301', '2026-10-24 12:36:11', 'El ratón óptico presenta fallas en el sensor y el cursor se desplaza de forma errática por la pantalla.', 'Hardware', 'Media', 0.002, 'Hardware', 'Media', 'Validado', NULL, '2026-10-24 17:41:07'),
(57, 'TICK-1550', '2026-10-24 12:36:17', 'El sistema ERP se bloquea por completo al intentar procesar el cierre mensual de planillas.', 'Software', 'Media', 0.001, 'Software', 'Crítica', 'Validado', NULL, '2026-10-24 17:40:49'),
(58, 'TICK-4158', '2026-10-24 12:36:24', 'La señal de red inalámbrica en la sala de juntas es demasiado débil para realizar videoconferencias.', 'Hardware', 'Alta', 0.002, 'Redes', 'Media', 'Validado', NULL, '2026-10-24 17:40:38'),
(59, 'TICK-4315', '2026-10-24 12:36:48', 'Asignación de permisos de lectura para un nuevo analista en la carpeta compartida de proyectos.', 'Hardware', 'Alta', 0.001, 'Accesos', 'Baja', 'Validado', NULL, '2026-10-24 17:40:18'),
(60, 'TICK-3080', '2026-10-24 12:37:06', 'La impresora principal de emisión de tickets está totalmente fuera de línea y no responde a la red.', 'Impresoras', 'Baja', 0.002, 'Impresoras', 'Crítica', 'Validado', NULL, '2026-10-24 17:40:00'),
(61, 'TICK-7633', '2026-10-24 12:51:59', 'No hay conexión a internet en la red Wi-Fi\"', 'Hardware', 'Media', 0.002, 'Redes', 'Media', 'Validado', NULL, '2026-10-24 18:19:42'),
(62, 'TICK-4224', '2026-10-24 12:53:16', 'No hay conexion a internet en la red Wi-fi', 'Hardware', 'Media', 0.001, 'Redes', 'Media', 'Validado', NULL, '2026-10-24 18:19:37'),
(63, 'TICK-8366', '2026-10-24 12:58:47', 'No hay conexion a internet en la red Wi-fi', 'Redes', 'Media', 0.017, 'Redes', 'Media', 'Validado', NULL, '2026-10-24 18:19:27'),
(64, 'TICK-2299', '2026-10-24 13:01:15', 'El usuario olvidó su contraseña de acceso al dominio de la red y su cuenta está bloqueada.', 'Accesos', 'Media', 0.001, 'Accesos', 'Media', 'Validado', NULL, '2026-10-24 18:19:09'),
(65, 'TICK-2970', '2026-10-24 13:01:21', 'La cuenta corporativa muestra el mensaje de usuario deshabilitado temporalmente por inactividad.', 'Accesos', 'Media', 0.001, 'Accesos', 'Baja', 'Validado', NULL, '2026-10-24 18:19:05'),
(66, 'TICK-8553', '2026-10-24 13:01:27', 'Se necesitan permisos temporales de administrador para instalar una herramienta aprobada por TI.', 'Accesos', 'Media', 0.002, 'Accesos', 'Media', 'Validado', NULL, '2026-10-24 18:18:42'),
(67, 'TICK-1150', '2026-10-24 13:01:40', 'La impresora multifuncional indica un error persistente de atasco de papel en la bandeja principal.', 'Impresoras', 'Media', 0.002, 'Impresoras', 'Media', 'Validado', NULL, '2026-10-24 18:17:20'),
(68, 'TICK-8372', '2026-10-24 13:01:52', 'El sistema de recursos humanos rechaza las credenciales de ingreso a pesar de ser correctas.', 'Accesos', 'Media', 0.002, 'Accesos', 'Alta', 'Validado', NULL, '2026-10-24 18:17:04'),
(69, 'TICK-7449', '2026-10-24 13:01:57', 'Es necesario solicitar la baja inmediata y desactivación de accesos para un ex colaborador.', 'Accesos', 'Media', 0.002, 'Accesos', 'Crítica', 'Validado', NULL, '2026-10-24 18:16:46'),
(70, 'TICK-9199', '2026-10-24 13:02:05', 'El tóner nuevo parpadea en rojo en el panel y el equipo se niega por completo a imprimir.', 'Hardware', 'Media', 0.002, 'Impresoras', 'Alta', 'Validado', NULL, '2026-10-24 18:14:10'),
(71, 'TICK-3115', '2026-10-24 13:02:14', 'Las impresiones salen con manchas negras horizontales y texto borroso en los bordes.', 'Redes', 'Media', 0.004, 'Impresoras', 'Baja', 'Validado', NULL, '2026-10-24 18:13:36'),
(72, 'TICK-2123', '2026-10-24 13:02:20', 'La impresora de etiquetas no alinea correctamente el texto en las cintas térmicas.', 'Impresoras', 'Media', 0.001, 'Impresoras', 'Media', 'Validado', NULL, '2026-10-24 18:13:21'),
(73, 'TICK-6171', '2026-10-24 13:02:26', 'El escáner en red de la fotocopiadora no envía los documentos digitalizados al correo del usuario.', 'Redes', 'Media', 0.001, 'Impresoras', 'Alta', 'Validado', NULL, '2026-10-24 18:13:09'),
(74, 'TICK-8161', '2026-10-24 13:02:36', 'No hay acceso a internet ni a las carpetas compartidas del servidor de la oficina.', 'Redes', 'Media', 0.002, 'Redes', 'Crítica', 'Validado', NULL, '2026-10-24 18:12:30'),
(75, 'TICK-1578', '2026-10-24 13:02:41', 'La conexión Wi-Fi se desconecta intermitentemente cada pocos minutos en el área comercial.', 'Redes', 'Media', 0.001, 'Redes', 'Media', 'Validado', NULL, '2026-10-24 18:12:23'),
(76, 'TICK-1855', '2026-10-24 13:02:45', 'El ping hacia la pasarela de pagos local tiene una latencia muy alta y se corta la señal.', 'Redes', 'Media', 0.001, 'Redes', 'Alta', 'Validado', NULL, '2026-10-24 18:12:05'),
(77, 'TICK-9815', '2026-10-24 13:02:49', 'La VPN corporativa se queda en estado de conectando y no logra autenticar el túnel seguro.', 'Redes', 'Media', 0.001, 'Redes', 'Alta', 'Validado', NULL, '2026-10-24 18:11:43'),
(78, 'TICK-8384', '2026-10-24 13:02:54', 'El puerto de red Ethernet del escritorio no enciende las luces de enlace al conectar el cable.', 'Hardware', 'Media', 0.001, 'Redes', 'Media', 'Validado', NULL, '2026-10-24 18:11:31'),
(79, 'TICK-5776', '2026-10-24 13:03:02', 'El navegador web se cierra inesperadamente al intentar abrir la plataforma principal de trabajo.', 'Software', 'Media', 0.001, 'Software', 'Media', 'Validado', NULL, '2026-10-24 18:11:17'),
(80, 'TICK-7620', '2026-10-24 13:03:06', 'Microsoft Excel arroja un error crítico de memoria insuficiente al abrir hojas de cálculo.', 'Software', 'Media', 0.001, 'Software', 'Alta', 'Validado', NULL, '2026-10-24 18:10:11'),
(81, 'TICK-8724', '2026-10-24 13:03:09', 'El sistema ERP no permite generar reportes y muestra un mensaje de excepción no controlada.', 'Software', 'Media', 0.001, 'Software', 'Crítica', 'Validado', NULL, '2026-10-24 18:09:52'),
(82, 'TICK-9808', '2026-10-24 13:03:16', 'La aplicación de videollamadas no detecta la cámara ni el micrófono integrado del equipo.', 'Hardware', 'Media', 0.002, 'Software', 'Media', 'Validado', NULL, '2026-10-24 18:09:38'),
(83, 'TICK-7553', '2026-10-24 13:03:22', 'El antivirus corporativo bloquea la ejecución de una macro necesaria para facturación.', 'Software', 'Media', 0.001, 'Software', 'Alta', 'Validado', NULL, '2026-10-24 18:09:15'),
(84, 'TICK-6312', '2026-10-24 13:03:28', 'La pantalla del monitor muestra líneas verticales de colores y se congela la imagen.', 'Hardware', 'Media', 0.001, 'Hardware', 'Media', 'Validado', NULL, '2026-10-24 18:07:55'),
(85, 'TICK-8869', '2026-10-24 13:03:31', 'El disco duro externo hace un ruido metálico extraño y no es reconocido por el equipo.', 'Hardware', 'Media', 0.002, 'Hardware', 'Crítica', 'Validado', NULL, '2026-10-24 18:07:44'),
(86, 'TICK-6519', '2026-10-24 13:03:35', 'El cargador de la laptop se sobrecalienta de forma excesiva y deja de suministrar energía.', 'Hardware', 'Media', 0.001, 'Hardware', 'Alta', 'Validado', NULL, '2026-10-24 18:07:33'),
(88, 'TICK-6651', '2026-10-24 13:04:32', 'La batería del equipo portátil no retiene carga y se apaga al desconectar el cable de corriente.', 'Hardware', 'Media', 0.002, 'Hardware', 'Alta', 'Validado', NULL, '2026-10-24 18:07:04'),
(89, 'TICK-1793213523', '2026-10-28 13:52:03', 'La computadora muestra pantalla azul y no se puede ingresar al escritorio ', 'Hardware', 'Media', 0.0391, 'Hardware', 'Crítica', 'Validado', NULL, '2026-10-28 18:53:42');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `rol` enum('Administrador','Analista','Cliente') NOT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `email`, `password_hash`, `rol`, `fecha_creacion`) VALUES
(1, 'Administrador General', 'admin@soporte.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Administrador', '2026-10-22 16:18:22'),
(2, 'Analista Soporte', 'analista@soporte.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Analista', '2026-10-22 16:18:22'),
(4, 'Administrador Master', 'admin@concentrix.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Administrador', '2026-10-23 16:13:59'),
(5, 'Enrique Gonzales', 'enriquefgch123@gmail.com', '$2y$10$Wh5u8Rc41k.d3vuKjCjItOk3LqgRW8Uo4kJ8XpmGK7aX5J2xI6O/2', 'Cliente', '2026-10-23 16:25:45'),
(6, 'Administrador Principal', 'admin2@concentrix.com', '$2y$10$NvT3MIvh6xMS1zVBr6fYCe3/qmkK0gBAyRa0mDAEa3EEykgjxgzwS', 'Administrador', '2026-10-23 16:47:49'),
(7, 'Wilfredo Gonzales', 'wgonzales7@gmail.com', '$2y$10$dVglso5D3iWmr0jOsEjYrORA/XfVAqwiX3NYE8UF27LlCRDMsgAV6', 'Analista', '2026-10-23 16:50:35'),
(8, 'Ana Martinez', 'karpashop123@gmail.com', '$2b$12$rdT3TYV5dvFiEAow/Ef.du.LZAfqypz2jKqBElWUqKgBFnnvu6C6K', 'Analista', '2026-10-28 18:33:45'),
(9, 'Enrique Gonzales', 'enriquefgch1234@gmail.com', '$2b$12$WA9r3HZGy79tSelhZ2hvd./Fy.KYrFH9mWQm5sKSEAKTXqhADKvxi', 'Cliente', '2026-10-28 18:49:02');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `incidencias`
--
ALTER TABLE `incidencias`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `codigo_ticket` (`codigo_ticket`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `incidencias`
--
ALTER TABLE `incidencias`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=90;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `incidencias`
--
ALTER TABLE `incidencias`
  ADD CONSTRAINT `incidencias_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
