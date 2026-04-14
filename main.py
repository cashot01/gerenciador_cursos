from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, FloatPrompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown

from models.professor import Professor
from models.aluno import Aluno
from models.curso import Curso
from services.gerenciador import GerenciadorCursos

console = Console()

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
        "[dim]Python POO + Rich CLI + JSON Persistence[/dim]",
        border_style="cyan",
        padding=(1, 2)
    ))

def menu_principal() -> int:
    console.print("\n[bold yellow]📋 Menu Principal:[/bold yellow]")
    opcoes = [
        "1. 👨‍🏫 Cadastrar Professor",
        "2. 👨‍🎓 Cadastrar Aluno",
        "3. 📚 Cadastrar Curso",
        "4. 📝 Matricular Aluno em Curso",
        "5. ❌ Desmatricular Aluno",
        "6. 📊 Adicionar Nota a Aluno",
        "7. 🔍 Listar Cursos",
        "8. 📈 Gerar Relatório de Turmas",
        "9. 💾 Salvar Dados Manualmente",
        "10. 🚪 Sair (Salva automaticamente)"
    ]
    for op in opcoes:
        console.print(f"  • {op}")
    return IntPrompt.ask("\n[bold green]Escolha uma opção[/bold green]", default=10)

def cadastrar_professor(professores: list[Professor]):
    console.print(Panel("👨‍🏫 [bold]Novo Professor[/bold]", border_style="blue"))
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

def cadastrar_aluno(alunos: list[Aluno]):
    console.print(Panel("👨‍🎓 [bold]Novo Aluno[/bold]", border_style="green"))
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

def cadastrar_curso(professores: list[Professor]):
    if not professores:
        console.print("  ⚠️ [yellow]Nenhum professor cadastrado. Cadastre um primeiro![/yellow]")
        return None
    console.print(Panel("📚 [bold]Novo Curso[/bold]", border_style="magenta"))
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

def listar_cursos():
    console.print(Panel("🔍 [bold]Cursos Cadastrados[/bold]", border_style="cyan"))
    cursos = GerenciadorCursos._cursos
    if not cursos:
        console.print("  📭 [dim]Nenhum curso cadastrado ainda.[/dim]")
        return
    table = Table(title="Catálogo de Cursos", show_header=True, header_style="bold cyan")
    table.add_column("Código", style="dim")
    table.add_column("Curso")
    table.add_column("Carga")
    table.add_column("Professor")
    table.add_column("Alunos", justify="right")
    for curso in cursos:
        table.add_row(curso.codigo, curso.nome, f"{curso.carga_horaria}h", curso.professor.nome, str(len(curso.alunos)))
    console.print(table)

def gerar_relatorio():
    console.print(Panel("📈 [bold]Relatório de Turmas[/bold]", border_style="magenta"))
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console, transient=True) as progress:
        progress.add_task("Gerando relatório...", total=None)
        relatorio = GerenciadorCursos.gerar_relatorio_turmas()
    console.print(Markdown(relatorio))

def main():
    # 1. Carregar dados existentes
    if GerenciadorCursos.carregar_dados():
        console.print("📂 [green]Dados carregados com sucesso do arquivo JSON![/green]")
    
    # 2. Extrair listas para o menu
    professores, alunos = extrair_listas_unicas()
    
    while True:
        limpar_tela()
        exibir_cabecalho()
        opcao = menu_principal()
        
        if opcao == 1:
            cadastrar_professor(professores)
        elif opcao == 2:
            cadastrar_aluno(alunos)
        elif opcao == 3:
            cadastrar_curso(professores)
        elif opcao == 4:
            matricular_aluno(alunos)
        elif opcao == 5:
            desmatricular_aluno()
        elif opcao == 6:
            adicionar_nota()
        elif opcao == 7:
            listar_cursos()
        elif opcao == 8:
            gerar_relatorio()
        elif opcao == 9:
            caminho = GerenciadorCursos.salvar_dados()
            console.print(f"💾 [green]Dados salvos em: {caminho}[/green]")
        elif opcao == 10:
            caminho = GerenciadorCursos.salvar_dados()
            console.print(Panel(f"\n[bold green]👋 Dados salvos em: {caminho}\nObrigado por usar o Sistema de Cursos![/bold green]\n", border_style="green"))
            break
        else:
            console.print("  ❌ [red]Opção inválida. Tente novamente.[/red]")
        
        Prompt.ask("\n[dim]Pressione Enter para continuar[/dim]")

if __name__ == "__main__":
    main()