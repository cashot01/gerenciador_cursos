from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, FloatPrompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown

from models.professor import Professor
from models.aluno import Aluno
from models.curso import Curso
from services.gerenciador import GerenciadorCursos

console = Console()

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def extrair_listas_unicas():
    """Extrai professores e alunos únicos de todos os cursos carregados."""
    professores = []
    alunos = []
    seen_prof_emails = set()
    seen_aluno_mats = set()
    
    for curso in GerenciadorCursos._cursos:
        if curso.professor.email not in seen_prof_emails:
            professores.append(curso.professor)
            seen_prof_emails.add(curso.professor.email)
        for aluno in curso.alunos:
            if aluno.matricula not in seen_aluno_mats:
                alunos.append(aluno)
                seen_aluno_mats.add(aluno.matricula)
    return professores, alunos

def limpar_tela():
    console.print("\n" * 2)

def exibir_cabecalho():
    console.print(Panel.fit(
        "🎓 [bold cyan]Sistema de Gerenciamento de Cursos[/bold cyan]\n"
        "[dim]Python POO + Rich CLI + JSON Persistence + CRUD Completo[/dim]",
        border_style="cyan",
        padding=(1, 2)
    ))

def voltar_ao_menu():
    Prompt.ask("\n[dim]Pressione Enter para continuar[/dim]")

# ============================================================================
# MENU PRINCIPAL
# ============================================================================

def menu_principal() -> int:
    console.print("\n[bold yellow]📋 Menu Principal:[/bold yellow]")
    opcoes = [
        "1. 👨‍🏫 Gerenciar Professores (CRUD)",
        "2. 👨‍🎓 Gerenciar Alunos (CRUD)",
        "3. 📚 Gerenciar Cursos (CRUD)",
        "4. 📝 Matricular Aluno em Curso",
        "5. ❌ Desmatricular Aluno",
        "6. 📊 Adicionar Nota a Aluno",
        "7. 🔍 Listar Todos os Cursos",
        "8. 📈 Gerar Relatório de Turmas",
        "9. 📤 Exportar Relatório para CSV",
        "10. 💾 Salvar Dados Manualmente",
        "11. 🚪 Sair (Salva automaticamente)"
    ]
    for op in opcoes:
        console.print(f"  • {op}")
    return IntPrompt.ask("\n[bold green]Escolha uma opção[/bold green]")

def menu_professores(professores: list[Professor]) -> int:
    console.print(Panel("[bold blue]👨‍🏫 Gerenciar Professores[/bold blue]", border_style="blue"))
    opcoes = [
        "1. ➕ Cadastrar Novo Professor",
        "2. 👁️ Listar Todos os Professores",
        "3. ✏️ Editar Professor",
        "4. 🗑️ Excluir Professor",
        "5. 🔙 Voltar ao Menu Principal"
    ]
    for op in opcoes:
        console.print(f"  • {op}")
    return IntPrompt.ask("\n[bold green]Escolha uma opção[/bold green]")

def menu_alunos(alunos: list[Aluno]) -> int:
    console.print(Panel("[bold green]👨‍🎓 Gerenciar Alunos[/bold green]", border_style="green"))
    opcoes = [
        "1. ➕ Cadastrar Novo Aluno",
        "2. 👁️ Listar Todos os Alunos",
        "3. ✏️ Editar Aluno",
        "4. 🗑️ Excluir Aluno",
        "5. 🔙 Voltar ao Menu Principal"
    ]
    for op in opcoes:
        console.print(f"  • {op}")
    return IntPrompt.ask("\n[bold green]Escolha uma opção[/bold green]")

def menu_cursos() -> int:
    console.print(Panel("[bold magenta]📚 Gerenciar Cursos[/bold magenta]", border_style="magenta"))
    opcoes = [
        "1. ➕ Cadastrar Novo Curso",
        "2. 👁️ Listar Todos os Cursos",
        "3. ✏️ Editar Curso",
        "4. 🗑️ Excluir Curso",
        "5. 🔙 Voltar ao Menu Principal"
    ]
    for op in opcoes:
        console.print(f"  • {op}")
    return IntPrompt.ask("\n[bold green]Escolha uma opção[/bold green]")

# ============================================================================
# CRUD PROFESSOR
# ============================================================================

def criar_professor(professores: list[Professor]) -> Professor | None:
    console.print(Panel("➕ [bold]Novo Professor[/bold]", border_style="blue"))
    nome = Prompt.ask("  Nome")
    email = Prompt.ask("  Email")
    especialidade = Prompt.ask("  Especialidade")
    try:
        prof = Professor(nome, email, especialidade)
        professores.append(prof)
        console.print(f"  ✅ [green]Professor '{prof.nome}' cadastrado![/green]")
        return prof
    except ValueError as e:
        console.print(f"  ❌ [red]Erro: {e}[/red]")
        return None

def listar_professores(professores: list[Professor]):
    console.print(Panel("👁️ [bold]Professores Cadastrados[/bold]", border_style="blue"))
    if not professores:
        console.print("  📭 [dim]Nenhum professor cadastrado.[/dim]")
        return
    table = Table(show_header=True, header_style="bold blue", show_lines=True)
    table.add_column("#", style="dim", width=3)
    table.add_column("Nome")
    table.add_column("Email")
    table.add_column("Especialidade")
    for i, p in enumerate(professores, 1):
        table.add_row(str(i), p.nome, p.email, p.especialidade)
    console.print(table)

def editar_professor(professores: list[Professor]):
    if not professores:
        console.print("  ⚠️ [yellow]Nenhum professor cadastrado.[/yellow]")
        return
    listar_professores(professores)
    idx = IntPrompt.ask("  Selecione o professor para editar", default=1) - 1
    if not (0 <= idx < len(professores)):
        console.print("  ❌ [red]Professor inválido[/red]")
        return
    prof = professores[idx]
    console.print(Panel(f"✏️ [bold]Editar: {prof.nome}[/bold]", border_style="yellow"))
    novo_nome = Prompt.ask("  Nome", default=prof.nome)
    novo_email = Prompt.ask("  Email", default=prof.email)
    nova_especialidade = Prompt.ask("  Especialidade", default=prof.especialidade)
    try:
        prof.nome = novo_nome
        prof.email = novo_email  # aciona validação do setter
        prof.especialidade = nova_especialidade
        console.print(f"  ✅ [green]Professor atualizado com sucesso![/green]")
    except ValueError as e:
        console.print(f"  ❌ [red]Erro: {e}[/red]")

def excluir_professor(professores: list[Professor], cursos: list[Curso]):
    if not professores:
        console.print("  ⚠️ [yellow]Nenhum professor cadastrado.[/yellow]")
        return
    listar_professores(professores)
    idx = IntPrompt.ask("  Selecione o professor para excluir", default=1) - 1
    if not (0 <= idx < len(professores)):
        console.print("  ❌ [red]Professor inválido[/red]")
        return
    prof = professores[idx]
    
    # Verificar se professor está vinculado a cursos
    cursos_vinculados = [c for c in cursos if c.professor.email == prof.email]
    if cursos_vinculados:
        console.print(f"  ⚠️ [yellow]Professor possui {len(cursos_vinculados)} curso(s) vinculado(s).[/yellow]")
        for c in cursos_vinculados:
            console.print(f"     - {c.codigo}: {c.nome}")
        if not Confirm.ask("  Deseja excluir mesmo assim? (cursos ficarão sem professor)"):
            console.print("  ⚪ [dim]Operação cancelada.[/dim]")
            return
    
    if Confirm.ask(f"  Confirmar exclusão de [red]{prof.nome}[/red]?"):
        professores.remove(prof)
        # Remover referência dos cursos
        for curso in cursos_vinculados:
            curso.professor = Professor("Não informado", "nao@informado.com", "N/A")
        console.print(f"  ✅ [green]Professor excluído com sucesso![/green]")
    else:
        console.print("  ⚪ [dim]Operação cancelada.[/dim]")

# ============================================================================
# CRUD ALUNO
# ============================================================================

def criar_aluno(alunos: list[Aluno]) -> Aluno | None:
    console.print(Panel("➕ [bold]Novo Aluno[/bold]", border_style="green"))
    nome = Prompt.ask("  Nome")
    email = Prompt.ask("  Email")
    try:
        aluno = Aluno(nome, email)
        alunos.append(aluno)
        console.print(f"  ✅ [green]Aluno '{aluno.nome}' cadastrado! Matrícula: [bold]{aluno.matricula}[/bold][/green]")
        return aluno
    except ValueError as e:
        console.print(f"  ❌ [red]Erro: {e}[/red]")
        return None

def listar_alunos(alunos: list[Aluno]):
    console.print(Panel("👁️ [bold]Alunos Cadastrados[/bold]", border_style="green"))
    if not alunos:
        console.print("  📭 [dim]Nenhum aluno cadastrado.[/dim]")
        return
    table = Table(show_header=True, header_style="bold green", show_lines=True)
    table.add_column("#", style="dim", width=3)
    table.add_column("Matrícula", style="cyan")
    table.add_column("Nome")
    table.add_column("Email")
    table.add_column("Média", justify="right")
    for i, a in enumerate(alunos, 1):
        table.add_row(str(i), a.matricula, a.nome, a.email, f"{a.calcular_media():.1f}")
    console.print(table)

def editar_aluno(alunos: list[Aluno]):
    if not alunos:
        console.print("  ⚠️ [yellow]Nenhum aluno cadastrado.[/yellow]")
        return
    listar_alunos(alunos)
    idx = IntPrompt.ask("  Selecione o aluno para editar", default=1) - 1
    if not (0 <= idx < len(alunos)):
        console.print("  ❌ [red]Aluno inválido[/red]")
        return
    aluno = alunos[idx]
    console.print(Panel(f"✏️ [bold]Editar: {aluno.nome} ({aluno.matricula})[/bold]", border_style="yellow"))
    novo_nome = Prompt.ask("  Nome", default=aluno.nome)
    novo_email = Prompt.ask("  Email", default=aluno.email)
    try:
        aluno.nome = novo_nome
        aluno.email = novo_email  # aciona validação do setter
        console.print(f"  ✅ [green]Aluno atualizado com sucesso![/green]")
    except ValueError as e:
        console.print(f"  ❌ [red]Erro: {e}[/red]")

def excluir_aluno(alunos: list[Aluno], cursos: list[Curso]):
    if not alunos:
        console.print("  ⚠️ [yellow]Nenhum aluno cadastrado.[/yellow]")
        return
    listar_alunos(alunos)
    idx = IntPrompt.ask("  Selecione o aluno para excluir", default=1) - 1
    if not (0 <= idx < len(alunos)):
        console.print("  ❌ [red]Aluno inválido[/red]")
        return
    aluno = alunos[idx]
    
    # Verificar matrículas ativas
    matriculas_ativas = []
    for curso in cursos:
        if aluno in curso.alunos:
            matriculas_ativas.append(curso)
    
    if matriculas_ativas:
        console.print(f"  ⚠️ [yellow]Aluno está matriculado em {len(matriculas_ativas)} curso(s):[/yellow]")
        for c in matriculas_ativas:
            console.print(f"     - {c.codigo}: {c.nome}")
        if not Confirm.ask("  Deseja excluir mesmo assim? (será desmatriculado automaticamente)"):
            console.print("  ⚪ [dim]Operação cancelada.[/dim]")
            return
        # Desmatricular automaticamente
        for curso in matriculas_ativas:
            curso.desmatricular(aluno)
        console.print("  📝 [dim]Aluno desmatriculado dos cursos automaticamente.[/dim]")
    
    if Confirm.ask(f"  Confirmar exclusão de [red]{aluno.nome}[/red] ({aluno.matricula})?"):
        alunos.remove(aluno)
        console.print(f"  ✅ [green]Aluno excluído com sucesso![/green]")
    else:
        console.print("  ⚪ [dim]Operação cancelada.[/dim]")

# ============================================================================
# CRUD CURSO
# ============================================================================

def criar_curso(professores: list[Professor]) -> Curso | None:
    if not professores:
        console.print("  ⚠️ [yellow]Nenhum professor cadastrado. Cadastre um primeiro![/yellow]")
        return None
    console.print(Panel("➕ [bold]Novo Curso[/bold]", border_style="magenta"))
    table = Table(title="Professores Disponíveis", show_lines=True)
    table.add_column("#", style="dim")
    table.add_column("Nome")
    table.add_column("Especialidade")
    for i, p in enumerate(professores, 1):
        table.add_row(str(i), p.nome, p.especialidade)
    console.print(table)
    idx = IntPrompt.ask("  Selecione o professor (número)", default=1) - 1
    if not (0 <= idx < len(professores)):
        console.print("  ❌ [red]Professor inválido[/red]")
        return None
    codigo = Prompt.ask("  Código do curso (ex: PY101)").upper()
    nome = Prompt.ask("  Nome do curso")
    carga = IntPrompt.ask("  Carga horária (horas)", default=40)
    curso = Curso(codigo, nome, carga, professores[idx])
    GerenciadorCursos.adicionar_curso(curso)
    console.print(f"  ✅ [green]Curso '{curso.nome}' cadastrado com sucesso![/green]")
    return curso

def listar_cursos():
    console.print(Panel("👁️ [bold]Cursos Cadastrados[/bold]", border_style="magenta"))
    cursos = GerenciadorCursos._cursos
    if not cursos:
        console.print("  📭 [dim]Nenhum curso cadastrado ainda.[/dim]")
        return
    table = Table(show_header=True, header_style="bold magenta", show_lines=True)
    table.add_column("#", style="dim", width=3)
    table.add_column("Código", style="cyan")
    table.add_column("Curso")
    table.add_column("Carga")
    table.add_column("Professor")
    table.add_column("Alunos", justify="right")
    for i, curso in enumerate(cursos, 1):
        table.add_row(
            str(i),
            curso.codigo,
            curso.nome,
            f"{curso.carga_horaria}h",
            curso.professor.nome,
            str(len(curso.alunos))
        )
    console.print(table)

def editar_curso(professores: list[Professor]):
    cursos = GerenciadorCursos._cursos
    if not cursos:
        console.print("  ⚠️ [yellow]Nenhum curso cadastrado.[/yellow]")
        return
    listar_cursos()
    idx = IntPrompt.ask("  Selecione o curso para editar", default=1) - 1
    if not (0 <= idx < len(cursos)):
        console.print("  ❌ [red]Curso inválido[/red]")
        return
    curso = cursos[idx]
    console.print(Panel(f"✏️ [bold]Editar: {curso.nome} ({curso.codigo})[/bold]", border_style="yellow"))
    
    # Selecionar novo professor
    console.print("\n[bold]Professores disponíveis:[/bold]")
    table = Table(show_lines=True)
    table.add_column("#", style="dim")
    table.add_column("Nome")
    table.add_column("Especialidade")
    for i, p in enumerate(professores, 1):
        table.add_row(str(i), p.nome, p.especialidade)
    console.print(table)
    idx_prof = IntPrompt.ask("  Selecione o professor", default=1) - 1
    if not (0 <= idx_prof < len(professores)):
        console.print("  ❌ [red]Professor inválido[/red]")
        return
    
    novo_nome = Prompt.ask("  Nome do curso", default=curso.nome)
    nova_carga = IntPrompt.ask("  Carga horária (horas)", default=curso.carga_horaria)
    
    curso.nome = novo_nome
    curso.carga_horaria = nova_carga
    curso.professor = professores[idx_prof]
    console.print(f"  ✅ [green]Curso atualizado com sucesso![/green]")

def excluir_curso():
    cursos = GerenciadorCursos._cursos
    if not cursos:
        console.print("  ⚠️ [yellow]Nenhum curso cadastrado.[/yellow]")
        return
    listar_cursos()
    idx = IntPrompt.ask("  Selecione o curso para excluir", default=1) - 1
    if not (0 <= idx < len(cursos)):
        console.print("  ❌ [red]Curso inválido[/red]")
        return
    curso = cursos[idx]
    
    if curso.alunos:
        console.print(f"  ⚠️ [yellow]Curso possui {len(curso.alunos)} aluno(s) matriculado(s).[/yellow]")
        if not Confirm.ask("  Deseja excluir mesmo assim? (alunos serão desmatriculados)"):
            console.print("  ⚪ [dim]Operação cancelada.[/dim]")
            return
        # Desmatricular todos automaticamente
        curso.alunos.clear()
        console.print("  📝 [dim]Todos os alunos foram desmatriculados automaticamente.[/dim]")
    
    if Confirm.ask(f"  Confirmar exclusão de [red]{curso.nome}[/red] ({curso.codigo})?"):
        GerenciadorCursos._cursos.remove(curso)
        console.print(f"  ✅ [green]Curso excluído com sucesso![/green]")
    else:
        console.print("  ⚪ [dim]Operação cancelada.[/dim]")

# ============================================================================
# OPERAÇÕES DE MATRÍCULA E NOTAS
# ============================================================================

def matricular_aluno(alunos: list[Aluno]):
    cursos = GerenciadorCursos._cursos
    if not cursos or not alunos:
        console.print("  ⚠️ [yellow]É necessário ter cursos e alunos cadastrados.[/yellow]")
        return
    console.print(Panel("📝 [bold]Matricular Aluno[/bold]", border_style="cyan"))
    console.print("\n[bold]Cursos disponíveis:[/bold]")
    for i, c in enumerate(cursos, 1):
        console.print(f"  {i}. {c.codigo} - {c.nome}")
    idx_curso = IntPrompt.ask("  Selecione o curso", default=1) - 1
    console.print("\n[bold]Alunos disponíveis:[/bold]")
    for i, a in enumerate(alunos, 1):
        console.print(f"  {i}. {a.matricula} - {a.nome}")
    idx_aluno = IntPrompt.ask("  Selecione o aluno", default=1) - 1
    try:
        cursos[idx_curso].matricular(alunos[idx_aluno])
        console.print(f"  ✅ [green]{alunos[idx_aluno].nome} matriculado em {cursos[idx_curso].nome}![/green]")
    except ValueError as e:
        console.print(f"  ❌ [red]Erro: {e}[/red]")

def desmatricular_aluno():
    cursos = GerenciadorCursos._cursos
    if not cursos:
        console.print("  ⚠️ [yellow]Nenhum curso disponível.[/yellow]")
        return
    console.print(Panel("❌ [bold]Desmatricular Aluno[/bold]", border_style="red"))
    cursos_com_alunos = [c for c in cursos if c.alunos]
    if not cursos_com_alunos:
        console.print("  ⚠️ [yellow]Nenhum curso com alunos matriculados.[/yellow]")
        return
    console.print("\n[bold]Cursos com matrículas:[/bold]")
    for i, c in enumerate(cursos_com_alunos, 1):
        console.print(f"  {i}. [cyan]{c.codigo}[/cyan] - {c.nome} ({len(c.alunos)} alunos)")
    idx_curso = IntPrompt.ask("  Selecione o curso", default=1) - 1
    if not (0 <= idx_curso < len(cursos_com_alunos)):
        console.print("  ❌ [red]Curso inválido[/red]")
        return
    curso = cursos_com_alunos[idx_curso]
    console.print(f"\n[bold]Alunos matriculados em [cyan]{curso.nome}[/cyan]:[/bold]")
    table = Table(show_header=True, header_style="bold red", show_lines=True)
    table.add_column("#", style="dim", width=3)
    table.add_column("Matrícula", style="cyan")
    table.add_column("Nome")
    table.add_column("Média", justify="right")
    for i, aluno in enumerate(curso.alunos, 1):
        table.add_row(str(i), aluno.matricula, aluno.nome, f"{aluno.calcular_media():.1f}")
    console.print(table)
    idx_aluno = IntPrompt.ask("  Selecione o aluno para desmatricular", default=1) - 1
    if not (0 <= idx_aluno < len(curso.alunos)):
        console.print("  ❌ [red]Aluno inválido[/red]")
        return
    aluno_selecionado = curso.alunos[idx_aluno]
    console.print(Panel(
        f"[bold]Confirmação[/bold]\n"
        f"Desmatricular [yellow]{aluno_selecionado.nome}[/yellow] ([cyan]{aluno_selecionado.matricula}[/cyan])\n"
        f"do curso [cyan]{curso.nome}[/cyan]?",
        border_style="yellow", padding=(1, 2)
    ))
    confirm = Prompt.ask("  Digite [bold]SIM[/bold] para confirmar", default="não").strip().upper()
    if confirm == "SIM":
        try:
            curso.desmatricular(aluno_selecionado)
            console.print(f"  ✅ [green]{aluno_selecionado.nome} desmatriculado com sucesso![/green]")
        except ValueError as e:
            console.print(f"  ❌ [red]Erro: {e}[/red]")
    else:
        console.print("  ⚪ [dim]Operação cancelada.[/dim]")

def adicionar_nota():
    cursos = GerenciadorCursos._cursos
    if not cursos:
        console.print("  ⚠️ [yellow]Nenhum curso disponível.[/yellow]")
        return
    console.print(Panel("📊 [bold]Adicionar Nota[/bold]", border_style="yellow"))
    cursos_com_alunos = [c for c in cursos if c.alunos]
    if not cursos_com_alunos:
        console.print("  ⚠️ [yellow]Nenhum curso com alunos matriculados.[/yellow]")
        return
    console.print("\n[bold]Cursos com alunos:[/bold]")
    for i, c in enumerate(cursos_com_alunos, 1):
        console.print(f"  {i}. {c.codigo} - {c.nome} ({len(c.alunos)} alunos)")
    idx = IntPrompt.ask("  Selecione o curso", default=1) - 1
    curso = cursos_com_alunos[idx]
    console.print("\n[bold]Alunos matriculados:[/bold]")
    for i, a in enumerate(curso.alunos, 1):
        console.print(f"  {i}. {a.matricula} - {a.nome} | Média atual: {a.calcular_media():.1f}")
    idx_aluno = IntPrompt.ask("  Selecione o aluno", default=1) - 1
    aluno = curso.alunos[idx_aluno]
    nota = FloatPrompt.ask("  Digite a nota (0.0 a 10.0)")
    try:
        aluno.adicionar_nota(nota)
        console.print(f"  ✅ [green]Nota {nota} adicionada! Nova média: {aluno.calcular_media():.1f}[/green]")
    except ValueError as e:
        console.print(f"  ❌ [red]Erro: {e}[/red]")

def gerar_relatorio():
    console.print(Panel("📈 [bold]Relatório de Turmas[/bold]", border_style="magenta"))
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console, transient=True) as progress:
        progress.add_task("Gerando relatório...", total=None)
        relatorio = GerenciadorCursos.gerar_relatorio_turmas()
    console.print(Markdown(relatorio))

def exportar_csv():
    cursos = GerenciadorCursos._cursos
    if not cursos:
        console.print("  ⚠️ [yellow]Nenhum curso cadastrado para exportar.[/yellow]")
        return
    
    console.print(Panel("📤 [bold]Exportar Relatório para CSV[/bold]", border_style="green"))
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("Exportando dados...", total=None)
        
        try:
            caminho = GerenciadorCursos.exportar_relatorio_csv()
            progress.update(task, completed=True)
            
            # Contar dados exportados
            total_alunos = sum(len(c.alunos) for c in cursos)
            total_cursos = len(cursos)
            
            console.print(Panel(
                f"[bold green]✅ Exportação concluída com sucesso![/bold green]\n\n"
                f"📁 Arquivo: [cyan]{caminho}[/cyan]\n"
                f"📊 Cursos exportados: [bold]{total_cursos}[/bold]\n"
                f"👨‍🎓 Total de matrículas: [bold]{total_alunos}[/bold]\n\n"
                f"[dim]Abra o arquivo no Excel, Google Sheets ou LibreOffice Calc.[/dim]",
                border_style="green",
                padding=(1, 2)
            ))
        except ValueError as e:
            console.print(f"  ❌ [red]Erro: {e}[/red]")
        except Exception as e:
            console.print(f"  ❌ [red]Erro inesperado: {e}[/red]")

# ============================================================================
# MAIN
# ============================================================================

def main():
    # 1. Carregar dados existentes
    if GerenciadorCursos.carregar_dados():
        console.print("📂 [green]Dados carregados com sucesso do arquivo JSON![/green]")
    
    # 2. Extrair listas para o menu
    professores, alunos = extrair_listas_unicas()
    cursos = GerenciadorCursos._cursos
    
    while True:
        limpar_tela()
        exibir_cabecalho()
        opcao = menu_principal()
        
        if opcao == 1:  # Gerenciar Professores
            while True:
                limpar_tela()
                sub_opcao = menu_professores(professores)
                if sub_opcao == 1:
                    criar_professor(professores)
                elif sub_opcao == 2:
                    listar_professores(professores)
                elif sub_opcao == 3:
                    editar_professor(professores)
                elif sub_opcao == 4:
                    excluir_professor(professores, cursos)
                elif sub_opcao == 5:
                    break
                voltar_ao_menu()
                
        elif opcao == 2:  # Gerenciar Alunos
            while True:
                limpar_tela()
                sub_opcao = menu_alunos(alunos)
                if sub_opcao == 1:
                    criar_aluno(alunos)
                elif sub_opcao == 2:
                    listar_alunos(alunos)
                elif sub_opcao == 3:
                    editar_aluno(alunos)
                elif sub_opcao == 4:
                    excluir_aluno(alunos, cursos)
                elif sub_opcao == 5:
                    break
                voltar_ao_menu()
                
        elif opcao == 3:  # Gerenciar Cursos
            while True:
                limpar_tela()
                sub_opcao = menu_cursos()
                if sub_opcao == 1:
                    criar_curso(professores)
                elif sub_opcao == 2:
                    listar_cursos()
                elif sub_opcao == 3:
                    editar_curso(professores)
                elif sub_opcao == 4:
                    excluir_curso()
                elif sub_opcao == 5:
                    break
                voltar_ao_menu()
                
        elif opcao == 4:
            matricular_aluno(alunos)
            voltar_ao_menu()
        elif opcao == 5:
            desmatricular_aluno()
            voltar_ao_menu()
        elif opcao == 6:
            adicionar_nota()
            voltar_ao_menu()
        elif opcao == 7:
            listar_cursos()
            voltar_ao_menu()
        elif opcao == 8:
            gerar_relatorio()
            voltar_ao_menu()
        elif opcao == 9:
            exportar_csv()
            voltar_ao_menu()
        elif opcao == 10:
            caminho = GerenciadorCursos.salvar_dados()
            console.print(f"💾 [green]Dados salvos em: {caminho}[/green]")
            voltar_ao_menu()
        elif opcao == 11:
            caminho = GerenciadorCursos.salvar_dados()
            console.print(Panel(f"\n[bold green]👋 Dados salvos em: {caminho}\nObrigado por usar o Sistema de Cursos![/bold green]\n", border_style="green"))
            break
        else:
            console.print("  ❌ [red]Opção inválida. Tente novamente.[/red]")
            voltar_ao_menu()

if __name__ == "__main__":
    main()