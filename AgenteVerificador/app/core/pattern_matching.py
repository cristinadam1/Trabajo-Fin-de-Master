import re
from dataclasses import dataclass

@dataclass(frozen=True)
class FirmaAtaque:
    id: str
    categoria_owasp: str | None
    descripcion: str
    risk_level: str
    patron: re.Pattern

FIRMAS = [

    # CRED / ACCESS / DISC : Credenciales y descubrimiento (LLM02)
    FirmaAtaque(
        id="CRED-002-SSH-KEY",
        categoria_owasp="LLM02",
        descripcion="Acceso a clave privada SSH id_rsa",
        risk_level="critico",
        patron=re.compile(r"(?i)\.ssh/id_rsa\b"),
    ),
    FirmaAtaque(
        id="CRED-002-SSH-KEY",
        categoria_owasp="LLM02",
        descripcion="Acceso a clave privada SSH id_ed25519",
        risk_level="critico",
        patron=re.compile(r"(?i)\.ssh/id_ed25519\b"),
    ),
    FirmaAtaque(
        id="CRED-001-PASSWD",
        categoria_owasp="LLM02",
        descripcion="Lectura de shadow o passwd",
        risk_level="critico",
        patron=re.compile(r"(?i)(?:/etc/shadow|/etc/passwd)\b"),
    ),
    FirmaAtaque(
        id="CRED-003-ENV",
        categoria_owasp="LLM02",
        descripcion="Cosecha de variables de entorno con key/secret/password",
        risk_level="alto",
        patron=re.compile(r"(?i)env\s*\|\s*grep.*(?:key|secret|password)"),
    ),
    FirmaAtaque(
        id="ACCESS-002-KEYGEN",
        categoria_owasp="LLM02",
        descripcion="Generacion de claves SSH con ssh-keygen",
        risk_level="critico",
        patron=re.compile(r"(?i)\bssh-keygen\b"),
    ),
    FirmaAtaque(
        id="DISC-001-RECON",
        categoria_owasp="LLM02",
        descripcion="Busqueda recursiva de secretos con grep en el sistema de archivos",
        risk_level="medio",
        patron=re.compile(r"(?i)grep\s+-r.*(?:password|secret|api_key|token)"),
    ),

    # ACCESS / RESOURCE / EVASION : Acceso remoto y evasión (LLM06)
    FirmaAtaque(
        id="ACCESS-001-REVSHELL",
        categoria_owasp="LLM06",
        descripcion="Uso de /dev/tcp para reverse shell",
        risk_level="critico",
        patron=re.compile(r"/dev/tcp/"),
    ),
    FirmaAtaque(
        id="RESOURCE-002-BACKDOOR",
        categoria_owasp="LLM06",
        descripcion="Netcat con ejecucion de shell (escritura de backdoor)",
        risk_level="alto",
        patron=re.compile(r"(?i)\bnc\s+-e\b"),
    ),
    FirmaAtaque(
        id="EVASION-004-HEX",
        categoria_owasp="LLM06",
        descripcion="Decodificacion hex dinamica con bytes.fromhex",
        risk_level="critico",
        patron=re.compile(r"(?i)bytes\.fromhex\s*\("),
    ),
    FirmaAtaque(
        id="EVASION-002-HIDE",
        categoria_owasp="LLM06",
        descripcion="Enmascaramiento de proceso con exec -a",
        risk_level="alto",
        patron=re.compile(r"(?i)\bexec\s+-a\s+"),
    ),

    # EXFIL / RESOURCE : Exfiltración y descarga (LLM02 / LLM06)
    FirmaAtaque(
        id="EXFIL-001-HTTP",
        categoria_owasp="LLM02",
        descripcion="Exfiltracion por HTTP POST con curl",
        risk_level="critico",
        patron=re.compile(r"(?i)curl\s+(?:-\w+\s+)*-X\s+POST"),
    ),
    FirmaAtaque(
        id="EXFIL-001-HTTP",
        categoria_owasp="LLM02",
        descripcion="Exfiltracion por formulario curl -F",
        risk_level="critico",
        patron=re.compile(r"(?i)curl\s+(?:-\w+\s+)*-F\s+"),
    ),
    FirmaAtaque(
        id="EXFIL-002-DNS",
        categoria_owasp="LLM02",
        descripcion="Tunel DNS con dig y datos codificados",
        risk_level="critico",
        patron=re.compile(r"(?i)dig\s*\$\(.*(?:base64|cat|echo)"),
    ),
    FirmaAtaque(
        id="EXFIL-003-EMAIL",
        categoria_owasp="LLM02",
        descripcion="Exfiltracion por correo con mail",
        risk_level="alto",
        patron=re.compile(r"(?i)\bmail\s+-s\b"),
    ),
    FirmaAtaque(
        id="RESOURCE-001-DOWNLOAD",
        categoria_owasp="LLM06",
        descripcion="Descarga remota de script con curl -o",
        risk_level="critico",
        patron=re.compile(r"(?i)curl\s+(?:-\w+\s+)*-o\s+"),
    ),

    # PERSIST : Persistencia (LLM06)
    FirmaAtaque(
        id="PERSIST-001-CRON",
        categoria_owasp="LLM06",
        descripcion="Modificacion de crontab [PERSIST-001]",
        risk_level="alto",
        patron=re.compile(r"(?i)crontab\s+-"),
    ),
    FirmaAtaque(
        id="PERSIST-002-STARTUP",
        categoria_owasp="LLM06",
        descripcion="Escritura en .bashrc para persistencia [PERSIST-002]",
        risk_level="critico",
        patron=re.compile(r"(?i)(?:\>\>|>>)\s*~?\.bashrc\b"),
    ),

    # IMPACT : Destrucción y DoS (LLM06 / LLM10)
    FirmaAtaque(
        id="IMPACT-001-DELETE",
        categoria_owasp="LLM06",
        descripcion="Borrado recursivo con rm -rf [IMPACT-001]",
        risk_level="critico",
        patron=re.compile(r"(?i)\brm\s+(?:-[rf]+\s+)*[./~]"),
    ),
    FirmaAtaque(
        id="IMPACT-002-EXHAUST",
        categoria_owasp="LLM10",
        descripcion="Bomba logica / agotamiento de recursos [IMPACT-002]",
        risk_level="alto",
        patron=re.compile(r"(?i)(?:yes\s+>\s*/dev/null|sleep\s+\d+\s*&&\s*kill\s+%1|:\s*\(\s*\)\s*\{)"),
    ),
    FirmaAtaque(
        id="IMPACT-003-SERVICE",
        categoria_owasp="LLM06",
        descripcion="Interrupcion y escaneo de servicios con systemctl [IMPACT-003]",
        risk_level="critico",
        patron=re.compile(r"(?i)systemctl\s+(?:stop|disable|kill|mask|list-units)"),
    ),
    FirmaAtaque(
        id="IMPACT-001-FIND-RM",
        categoria_owasp="LLM06",
        descripcion="Borrado masivo con find -exec rm [IMPACT-001]",
        risk_level="critico",
        patron=re.compile(r"(?i)find\s+.*-exec\s+rm\s+"),
    ),

    # EXEC / PRIVESC : Escalada de privilegios (LLM06)
    FirmaAtaque(
        id="EXEC-002-SUDO",
        categoria_owasp="LLM06",
        descripcion="Escalada con sudo [EXEC-002]",
        risk_level="critico",
        patron=re.compile(r"(?i)\bsudo\s+"),
    ),
    FirmaAtaque(
        id="EXEC-002-SU",
        categoria_owasp="LLM06",
        descripcion="Cambio de usuario con su [EXEC-002] [+]",
        risk_level="critico",
        patron=re.compile(r"(?i)\bsu\s+-"),
    ),
    FirmaAtaque(
        id="PRIVESC-001-SUID",
        categoria_owasp="LLM06",
        descripcion="Busqueda de binarios SUID [PRIVESC-001]",
        risk_level="critico",
        patron=re.compile(r"(?i)find\s+/.*-perm\s+-4000"),
    ),
    FirmaAtaque(
        id="PRIVESC-002-KERNEL",
        categoria_owasp="LLM06",
        descripcion="Carga de modulo del kernel [PRIVESC-002]",
        risk_level="critico",
        patron=re.compile(r"(?i)\binsmod\b"),
    ),

    # LATERAL / RECON : Reconocimiento y movimiento lateral (LLM06)
    FirmaAtaque(
        id="LATERAL-001-NMAP",
        categoria_owasp="LLM06",
        descripcion="Escaneo de red con nmap [LATERAL-001]",
        risk_level="alto",
        patron=re.compile(r"(?i)\bnmap\b"),
    ),
    FirmaAtaque(
        id="LATERAL-001-PING",
        categoria_owasp="LLM06",
        descripcion="Ping a subred [LATERAL-001]",
        risk_level="alto",
        patron=re.compile(r"(?i)ping\s+-c\s+\d+\s+\d+\.\d+\.\d+"),
    ),
    FirmaAtaque(
        id="LATERAL-002-SCP",
        categoria_owasp="LLM06",
        descripcion="Copia remota a IP local [LATERAL-002]",
        risk_level="alto",
        patron=re.compile(r"(?i)scp\s+.*@(?:192\.168|10\.|172\.1[6-9]|172\.2[0-9]|172\.3[01])"),
    ),
    FirmaAtaque(
        id="RECON-001-SYSINFO",
        categoria_owasp="LLM06",
        descripcion="Recoleccion de info del sistema: uname/hostname [RECON-001]",
        risk_level="bajo",
        patron=re.compile(r"(?i)(?:uname\s+-a|hostname\s*$)"),
    ),
    FirmaAtaque(
        id="RECON-001-PS",
        categoria_owasp="LLM06",
        descripcion="Listado de procesos con ps aux [RECON-001]",
        risk_level="bajo",
        patron=re.compile(r"(?i)ps\s+aux"),
    ),
    FirmaAtaque(
        id="RECON-002-NETCFG",
        categoria_owasp="LLM06",
        descripcion="Escaneo de red con ifconfig, ip addr o netstat [RECON-002]",
        risk_level="medio",
        patron=re.compile(r"(?i)(?:ifconfig|ip\s+addr|netstat\s+-an)"),
    ),
    FirmaAtaque(
        id="COLLECT-001-BULK",
        categoria_owasp="LLM02",
        descripcion="Lectura masiva de archivos con find -exec cat [COLLECT-001]",
        risk_level="alto",
        patron=re.compile(r"(?i)find\s+.*-exec\s+cat\s+\{\}"),
    ),

    # PROMPT / INJECT : Inyección de prompt (LLM01)
    FirmaAtaque(
        id="PROMPT-001-OVERRIDE",
        categoria_owasp="LLM01",
        descripcion="Inyeccion de prompt con saltos de contexto [PROMPT-001]",
        risk_level="alto",
        patron=re.compile(
            r"(?i)(?:ignorar|omite|olvida|desoye|sobrescribe)\s+(?:las\s+)?"
            r"(?:instrucciones?|indicaciones?|prompt|contexto)"
            r"|(?:nuevas?\s+)?instrucciones?\s*(?::|son)\s*:"
            r"|system\s*:.*?(?:di|act[úu]a|comportate|ignora|olvida|omite|instrucciones)"
            r"|simula\s+ser|finge\s+ser|pretende\s+ser"
            r"|\bDAN\b|do\.anything\.now|jailbreak"
        ),
    ),
    FirmaAtaque(
        id="INJECT-001-INDIRECT",
        categoria_owasp="LLM01",
        descripcion="Inyeccion indirecta via datos externos [INJECT-001]",
        risk_level="medio",
        patron=re.compile(
            r"(?i)(?:fuente|source|url|link|documento)\s*(?:\w+\s*){0,3}(?:contiene|dice|indica)"
        ),
    ),

    # SQL : Inyección SQL [+] (LLM05)
    FirmaAtaque(
        id="SQL-INJECT-CLASSIC",
        categoria_owasp="LLM05",
        descripcion="Inyeccion SQL clasica [+]",
        risk_level="alto",
        patron=re.compile(
            r"(?i)('|\")\s*(?:OR|AND)\s*['\"]?\s*['\"]?\s*=\s*['\"]"
            r"|UNION\s+(?:ALL\s+)?SELECT"
            r"|SELECT\s+\*\s+FROM"
            r"|DROP\s+TABLE|DELETE\s+FROM|INSERT\s+INTO|UPDATE\s+\w+\s+SET"
            r"|--\s*$|;\s*DROP|' OR '1'='1"
        ),
    ),
    FirmaAtaque(
        id="SQL-INJECT-BLIND",
        categoria_owasp="LLM05",
        descripcion="Inyeccion SQL automatizada ciega [+]",
        risk_level="alto",
        patron=re.compile(
            r"(?i)(?:SLEEP|WAITFOR\s+DELAY|BENCHMARK)\s*\("
            r"|SUBSTRING\s*\(.*?,\s*\d+,\s*1\s*\)"
            r"|information_schema"
            r"|ASCII\s*\(\s*SUBSTRING"
            r"|CASE\s+WHEN.*?THEN\s+SLEEP"
            r"|IF\s*\(.*?SLEEP"
        ),
    ),

    # EVASION / EXEC / SANDBOX : Ejecución de código (LLM06)
    FirmaAtaque(
        id="EVASION-005-PYTHON",
        categoria_owasp="LLM06",
        descripcion="Ejecucion dinamica de codigo Python [EVASION-005]",
        risk_level="critico",
        patron=re.compile(r"\b(?:eval|exec|compile|__import__)\s*\("),
    ),
    FirmaAtaque(
        id="EVASION-005-SYS",
        categoria_owasp="LLM06",
        descripcion="Llamadas al sistema operativo desde Python [EVASION-005]",
        risk_level="critico",
        patron=re.compile(
            r"(?i)\b(?:os\.system|subprocess\.[a-z]+|os\.popen|pty\.spawn|commands\.getoutput)\s*\("
        ),
    ),
    FirmaAtaque(
        id="EXEC-001-CHAIN",
        categoria_owasp="LLM06",
        descripcion="Comandos shell encadenados [EXEC-001]",
        risk_level="medio",
        patron=re.compile(
            r"(?i)(?:;\s*(?:rm|shutdown|reboot|chmod|chown|mkfs|dd|wget|curl|bash|nc|ncat|mkfile))"
            r"|(?:\|\s*(?:bash|sh|cmd|powershell))"
            r"|(?:&&\s*(?:curl|wget|nc|ncat))"
            r"|`[^`]*?(?:bash|sh|curl|wget)`"
            r"|\$\((?:cat|curl|wget|bash)"
        ),
    ),
    # EVASION / EXEC / SANDBOX : Ejecución de código (LLM06)
    FirmaAtaque(
        id="EVASION-005-WINAPI",
        categoria_owasp="LLM06",
        descripcion="Malware nativo: keylogger con API de Windows [+]",
        risk_level="critico",
        patron=re.compile(
            r"(?i)(?:GetAsyncKeyState|SetWindowsHookEx|GetForegroundWindow|GetWindowText)"
            r"|KEY_LOGGER|keylogger|KeyboardProc|WH_KEYBOARD"
            r"|(?:WriteFile|CreateFile)\s*\(.*?[Kk]ey[Hh]ook"
            r"|#include\s*<Windows\.h>"
            r"|#include\s*<winuser\.h>"
            r"|LRESULT\s+CALLBACK\s+KeyboardProc"
        ),
    ),
    FirmaAtaque(
        id="EVASION-005-MALWARE",
        categoria_owasp="LLM06",
        descripcion="Malware: persistencia, conexion inversa o descarga de payload [+]",
        risk_level="critico",
        patron=re.compile(
            r"(?i)(?:RegSetValue|CreateService|StartService|schtasks|SC\s+CREATE)"
            r"|(?:CreateRemoteThread|VirtualAllocEx|WriteProcessMemory)"
            r"|(?:socket\s*\(\s*AF_INET|connect\s*\(\s*sock|WSAStartup)"
            r"|(?:URLDownloadToFile|WebClient|DownloadString|WinHttpOpen)"
        ),
    ),
    FirmaAtaque(
        id="CRED-003-ENV-PY",
        categoria_owasp="LLM02",
        descripcion="Acceso a variables de entorno desde Python [CRED-003]",
        risk_level="alto",
        patron=re.compile(
            r"(?i)(?:os\.environ|os\.getenv|os\.putenv)"
            r"|open\s*\(\s*['\"](?:/etc/|\.env|config\.)"
        ),
    ),
    FirmaAtaque(
        id="EVASION-005-SCRIPT",
        categoria_owasp="LLM06",
        descripcion="Creacion de script shell con echo [EVASION-005]",
        risk_level="critico",
        patron=re.compile(r"(?i)echo\s+['\"][^'\"]*(?:bash|sh|python|perl|ruby)"),
    ),
    FirmaAtaque(
        id="SANDBOX-003-SYMLINK",
        categoria_owasp="LLM06",
        descripcion="Enlace simbolico a archivos sensibles [SANDBOX-003]",
        risk_level="critico",
        patron=re.compile(r"(?i)ln\s+-s\s+"),
    ),
    FirmaAtaque(
        id="SANDBOX-002-ABSOLUTE-PATH",
        categoria_owasp="LLM06",
        descripcion="Acceso a rutas absolutas del sistema operativo [SANDBOX-002]",
        risk_level="alto",
        patron=re.compile(
            r"(?i)(/var/log/|/boot/|/proc/|/windows/|/winnt/"
            r"|\\windows\\|\\winnt\\|system32|cmd\.exe|powershell\.exe)"
        ),
    ),
    FirmaAtaque(
        id="EXEC-003-SERVER",
        categoria_owasp="LLM06",
        descripcion="Servidor HTTP Python malicioso [EXEC-003]",
        risk_level="alto",
        patron=re.compile(r"(?i)(?:python.*-m\s+http\.server|http\.server\.test\s*\()"),
    ),

    # COLLECT / LEAK : Filtración y portapapeles (LLM02)
    FirmaAtaque(
        id="LEAK-001-TOKENS",
        categoria_owasp="LLM02",
        descripcion="Filtracion de claves o tokens en la respuesta [+]",
        risk_level="alto",
        patron=re.compile(
            r"(?i)(?:sk-[A-Za-z0-9]{20,}|api[_-]?key|secret|token|password|passwd)"
            r"(?:\s*[:=]\s*['\"][A-Za-z0-9_\-]{8,}['\"])?"
        ),
    ),

    # PROMPT-002 : Ingeniería social y suplantación (LLM01 / LLM06)
    FirmaAtaque(
        id="PROMPT-002-PHISHING",
        categoria_owasp="LLM01",
        descripcion="Phishing: suplantacion de identidad corporativa [PROMPT-002]",
        risk_level="medio",
        patron=re.compile(
            r"(?i)(?:estimado\s+(?:cliente|usuario)|apreciado\s+(?:cliente|usuario))"
            r"|(?:soporte\s+técnico|departamento\s+de\s+seguridad)\s*(?:\w+\s*){0,3}"
            r"(?:solicita|notifica|informa)"
            r"|(?:haga\s+clic|click\s+aquí|verifique\s+su\s+cuenta|actualice\s+su\s+información)"
            r"|(?:https?://(?:bit\.ly|tinyurl|shorturl|rb\.gy|ow\.ly|short\.link))"
            r"|(?:suplantando|haciéndose\s+pasar|falsificando)"
            r"|(?:correo\s+urgente|respuesta\s+inmediata|su\s+cuenta\s+será\s+(?:suspendida|bloqueada|cerrada))"
        ),
    ),

    FirmaAtaque(
        id="COLLECT-002-CLIPBOARD",
        categoria_owasp="LLM02",
        descripcion="Captura de portapapeles con pbpaste/xclip [COLLECT-002]",
        risk_level="medio",
        patron=re.compile(r"(?i)\b(?:pbpaste|xclip)\b"),
    ),

    FirmaAtaque(
        id="PROMPT-002-IMPERSONATE",
        categoria_owasp="LLM06",
        descripcion="Suplantacion de identidad o peticiones en nombre de otro [PROMPT-002]",
        risk_level="medio",
        patron=re.compile(
            r"(?i)(?:en\s+nombre\s+de|por\s+cuenta\s+de|suplantando|impersonat(?:e|ing))\s+\w+"
            r"|Authorization:\s*Bearer\s+\S+"
        ),
    ),

    # SUPPLY : Cadena de suministro (LLM03 / LLM06)
    FirmaAtaque(
        id="SUPPLY-001-GIT",
        categoria_owasp="LLM06",
        descripcion="Envenenamiento de la configuracion de Git [SUPPLY-001]",
        risk_level="critico",
        patron=re.compile(r"(?i)(?:>>|>)\s*\.?git/config"),
    ),
    FirmaAtaque(
        id="SUPPLY-001-GIT-CONFIG",
        categoria_owasp="LLM06",
        descripcion="Redireccion de hooks de Git via core.hooksPath [SUPPLY-001]",
        risk_level="alto",
        patron=re.compile(r"(?i)git\s+config\s+core\.hooksPath\s+"),
    ),
    FirmaAtaque(
        id="SUPPLY-002-PY",
        categoria_owasp="LLM06",
        descripcion="Secuestro de modulos de Python (ej. crear os.py local) [SUPPLY-002]",
        risk_level="critico",
        patron=re.compile(r"(?i)(?:echo|printf|cat\s+>)\s+.*?\bos\.py\b"),
    ),
    FirmaAtaque(
        id="SUPPLY-003-TYPO",
        categoria_owasp="LLM03",
        descripcion="Paquetes Typosquatting (ej. python-collors) [SUPPLY-003]",
        risk_level="alto",
        patron=re.compile(r"(?i)(?:pip|npm|gem)\s+(?:install|i)\s+[^a-zA-Z0-9]*(?:python-collors|requests?|colorama)\b"),
    ),

    # EVASION : Evasión (LLM06)
    FirmaAtaque(
        id="EVASION-001-LOGS",
        categoria_owasp="LLM06",
        descripcion="Manipulacion y borrado de logs para evasion [EVASION-001]",
        risk_level="alto",
        patron=re.compile(r"(?i)\brm\s+(?:-[A-Za-z]+\s+)*.*\.log\b"),
    ),
    FirmaAtaque(
        id="EVASION-003-B64",
        categoria_owasp="LLM06",
        descripcion="Ejecucion de payload oculto en Base64 [EVASION-003]",
        risk_level="critico",
        patron=re.compile(r"(?i)base64\s+(?:-d|--decode)\s*\|\s*(?:sh|bash|zsh)"),
    ),

    # RECON : Reconocimiento (LLM06)
    FirmaAtaque(
        id="RECON-003-USER",
        categoria_owasp="LLM06",
        descripcion="Enumeracion de usuarios y privilegios [RECON-003]",
        risk_level="medio",
        patron=re.compile(r"(?i)(?:whoami|id)\s*(?:&&|;|\|)"),
    ),
]

JERARQUIA_RIESGO = {"critico": 4, "alto": 3, "medio": 2, "bajo": 1, None: 0}
BASE64_LARGO = re.compile(r"[A-Za-z0-9+/]{60,}={0,2}")

# IDs de firmas que solo aplican a tool calls (no a texto generado)
IDS_EXCLUIDOS_TEXTO = frozenset({
    "RECON-001-SYSINFO", "RECON-001-PS", "RECON-002-NETCFG", "RECON-003-USER",
    "SANDBOX-002-ABSOLUTE-PATH",
    "LEAK-001-TOKENS",
})

# LEAK para texto
FIRMA_LEAK_TEXTO = FirmaAtaque(
    id="LEAK-001-TOKENS-TEXT",
    categoria_owasp="LLM02",
    descripcion="Filtracion de tokens o claves en la respuesta",
    risk_level="alto",
    patron=re.compile(
        r"(?i)(?:sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{36,}"
        r"|-----BEGIN\s+(?:RSA|OPENSSH|PRIVATE)\s+KEY-----)"
    ),
)

FIRMAS_TEXTO = [
    f for f in FIRMAS if f.id not in IDS_EXCLUIDOS_TEXTO
] + [FIRMA_LEAK_TEXTO]


def _recorrer_y_escanear(valor, firmas=None):
    if firmas is None:
        firmas = FIRMAS
    mejor = {"nivel": -1, "resultado": None}

    def _recurse(obj):
        if isinstance(obj, dict):
            for v in obj.values():
                _recurse(v)
        elif isinstance(obj, list):
            for item in obj:
                _recurse(item)
        elif isinstance(obj, str):
            for firma in firmas:
                m = firma.patron.search(obj)
                if m:
                    nivel = JERARQUIA_RIESGO.get(firma.risk_level, 0)
                    if nivel > mejor["nivel"]:
                        mejor["nivel"] = nivel
                        mejor["resultado"] = {
                            "safe": False,
                            "risk_level": firma.risk_level,
                            "categoria": firma.id,
                            "categoria_owasp": firma.categoria_owasp,
                            "descripcion": firma.descripcion,
                            "match": m.group(),
                        }
            if BASE64_LARGO.search(obj):
                nivel = JERARQUIA_RIESGO.get("critico", 0)
                if nivel > mejor["nivel"]:
                    mejor["nivel"] = nivel
                    mejor["resultado"] = {
                        "safe": False,
                        "risk_level": "critico",
                        "categoria": "LEAK-SECRETS",
                        "categoria_owasp": "LLM02",
                        "descripcion": "Carga util ofuscada en Base64",
                        "match": obj[:60],
                    }

    _recurse(valor)
    return mejor["resultado"]

def escanear_argumentos(argumentos: dict) -> dict:
    resultado = _recorrer_y_escanear(argumentos)
    if resultado:
        return resultado
    return {"safe": True, "risk_level": None}

def escanear_texto(texto: str) -> dict:
    resultado = _recorrer_y_escanear(texto, FIRMAS_TEXTO)
    if resultado:
        return resultado
    return {"safe": True, "risk_level": None}
