import os
import queue
import shlex
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText


class GitHelperApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Git Helper - Projeto em Equipe")
        self.root.geometry("1100x760")
        self.root.minsize(980, 680)

        self.repo_path = tk.StringVar(value=os.getcwd())
        self.current_branch_var = tk.StringVar(value="-")
        self.upstream_var = tk.StringVar(value="-")
        self.local_status_var = tk.StringVar(value="-")
        self.remote_status_var = tk.StringVar(value="-")
        self.branch_select_var = tk.StringVar(value="")
        self.commit_message_var = tk.StringVar(value="")

        self.command_queue: queue.Queue[tuple[str, str, str]] = queue.Queue()

        self._build_ui()
        self.root.after(150, self._process_queue)
        self.refresh_all()

    # ==========================
    # Interface
    # ==========================
    def _build_ui(self) -> None:
        top = ttk.Frame(self.root, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="Repositório:").grid(row=0, column=0, sticky="w")
        repo_entry = ttk.Entry(top, textvariable=self.repo_path, width=90)
        repo_entry.grid(row=0, column=1, padx=8, sticky="ew")

        ttk.Button(top, text="Selecionar pasta", command=self.select_repo).grid(row=0, column=2, padx=4)
        ttk.Button(top, text="Atualizar", command=self.refresh_all).grid(row=0, column=3, padx=4)

        top.columnconfigure(1, weight=1)

        info = ttk.LabelFrame(self.root, text="Resumo do repositório", padding=10)
        info.pack(fill="x", padx=10, pady=(0, 10))

        ttk.Label(info, text="Branch atual:").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        ttk.Label(info, textvariable=self.current_branch_var).grid(row=0, column=1, sticky="w", padx=5, pady=4)

        ttk.Label(info, text="Upstream:").grid(row=0, column=2, sticky="w", padx=5, pady=4)
        ttk.Label(info, textvariable=self.upstream_var).grid(row=0, column=3, sticky="w", padx=5, pady=4)

        ttk.Label(info, text="Status local:").grid(row=1, column=0, sticky="w", padx=5, pady=4)
        ttk.Label(info, textvariable=self.local_status_var).grid(row=1, column=1, sticky="w", padx=5, pady=4)

        ttk.Label(info, text="Status remoto:").grid(row=1, column=2, sticky="w", padx=5, pady=4)
        ttk.Label(info, textvariable=self.remote_status_var).grid(row=1, column=3, sticky="w", padx=5, pady=4)

        actions = ttk.LabelFrame(self.root, text="Ações principais", padding=10)
        actions.pack(fill="x", padx=10, pady=(0, 10))

        ttk.Label(actions, text="Trocar para branch:").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        self.branch_combo = ttk.Combobox(actions, textvariable=self.branch_select_var, width=35, state="readonly")
        self.branch_combo.grid(row=0, column=1, sticky="w", padx=5, pady=4)
        ttk.Button(actions, text="Trocar branch", command=self.checkout_branch).grid(row=0, column=2, padx=5, pady=4)

        ttk.Button(actions, text="Fetch remoto", command=self.fetch_remote).grid(row=0, column=3, padx=5, pady=4)
        ttk.Button(actions, text="Pull branch atual", command=self.pull_current_branch).grid(row=0, column=4, padx=5, pady=4)
        ttk.Button(actions, text="Push branch atual", command=self.push_current_branch).grid(row=0, column=5, padx=5, pady=4)

        commit_frame = ttk.LabelFrame(self.root, text="Commit", padding=10)
        commit_frame.pack(fill="x", padx=10, pady=(0, 10))

        ttk.Label(commit_frame, text="Mensagem:").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        ttk.Entry(commit_frame, textvariable=self.commit_message_var, width=90).grid(row=0, column=1, padx=5, pady=4, sticky="ew")
        ttk.Button(commit_frame, text="Add + Commit", command=self.add_and_commit).grid(row=0, column=2, padx=5, pady=4)

        commit_frame.columnconfigure(1, weight=1)

        middle = ttk.PanedWindow(self.root, orient="horizontal")
        middle.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        left_box = ttk.LabelFrame(middle, text="Arquivos modificados", padding=8)
        right_box = ttk.LabelFrame(middle, text="Log / saída dos comandos", padding=8)
        middle.add(left_box, weight=1)
        middle.add(right_box, weight=2)

        self.files_list = tk.Listbox(left_box, height=18)
        self.files_list.pack(fill="both", expand=True)

        self.log_text = ScrolledText(right_box, wrap="word", height=20)
        self.log_text.pack(fill="both", expand=True)
        self.log_text.configure(state="disabled")

        footer = ttk.LabelFrame(self.root, text="Boas práticas", padding=10)
        footer.pack(fill="x", padx=10, pady=(0, 10))

        tips = (
            "1. Não commitar direto na main.\n"
            "2. Trabalhar em branches de funcionalidade.\n"
            "3. Dar fetch/refresh antes de iniciar o dia.\n"
            "4. Se houver arquivos não commitados, evitar trocar de branch sem revisar.\n"
            "5. Este app NÃO faz merge automático nem resolve conflitos."
        )
        ttk.Label(footer, text=tips, justify="left").pack(anchor="w")

    # ==========================
    # Utilidades Git
    # ==========================
    def run_git_command(self, args: list[str]) -> tuple[bool, str, str]:
        repo = self.repo_path.get().strip()
        if not repo:
            return False, "", "Caminho do repositório está vazio."

        try:
            completed = subprocess.run(
                ["git", *args],
                cwd=repo,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                shell=False,
            )
            success = completed.returncode == 0
            return success, completed.stdout.strip(), completed.stderr.strip()
        except FileNotFoundError:
            return False, "", "Git não foi encontrado no sistema. Instale o Git e adicione ao PATH."
        except Exception as exc:
            return False, "", f"Erro ao executar comando Git: {exc}"

    def append_log(self, message: str) -> None:
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def clear_files_list(self) -> None:
        self.files_list.delete(0, "end")

    def is_git_repository(self) -> bool:
        ok, out, err = self.run_git_command(["rev-parse", "--is-inside-work-tree"])
        if not ok or out.lower() != "true":
            messagebox.showerror("Erro", f"A pasta selecionada não é um repositório Git válido.\n\nDetalhes: {err or out}")
            return False
        return True

    def has_uncommitted_changes(self) -> bool:
        ok, out, _ = self.run_git_command(["status", "--porcelain"])
        return bool(ok and out.strip())

    def get_current_branch(self) -> str:
        ok, out, _ = self.run_git_command(["branch", "--show-current"])
        return out.strip() if ok and out.strip() else "-"

    def get_upstream_branch(self) -> str:
        ok, out, _ = self.run_git_command(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"])
        return out.strip() if ok and out.strip() else "Sem upstream"

    def warn_if_sensitive_branch(self, action_name: str) -> bool:
        current = self.get_current_branch().lower()
        if current in {"main", "master", "develop", "desenvolvimento"}:
            return messagebox.askyesno(
                "Atenção",
                f"Você está na branch '{current}'.\n\n"
                f"Tem certeza que deseja continuar com a ação: {action_name}?",
            )
        return True

    # ==========================
    # Atualização de tela
    # ==========================
    def refresh_all(self) -> None:
        if not self.is_git_repository():
            return

        self.update_branch_info()
        self.update_branch_list()
        self.update_modified_files()
        self.check_remote_updates(silent=True)
        self.append_log("[INFO] Tela atualizada com sucesso.")

    def update_branch_info(self) -> None:
        branch = self.get_current_branch()
        upstream = self.get_upstream_branch()
        self.current_branch_var.set(branch)
        self.upstream_var.set(upstream)

        ok, out, _ = self.run_git_command(["status", "--short"])
        if ok:
            self.local_status_var.set("Há alterações locais" if out.strip() else "Sem alterações locais")
        else:
            self.local_status_var.set("Não foi possível verificar")

    def update_branch_list(self) -> None:
        ok, out, err = self.run_git_command(["branch", "--format=%(refname:short)"])
        if not ok:
            self.append_log(f"[ERRO] Não foi possível listar branches. {err}")
            return

        branches = [line.strip() for line in out.splitlines() if line.strip()]
        self.branch_combo["values"] = branches

        current = self.get_current_branch()
        if current in branches:
            self.branch_select_var.set(current)
        elif branches:
            self.branch_select_var.set(branches[0])
        else:
            self.branch_select_var.set("")

    def update_modified_files(self) -> None:
        self.clear_files_list()
        ok, out, err = self.run_git_command(["status", "--short"])
        if not ok:
            self.append_log(f"[ERRO] Não foi possível obter arquivos modificados. {err}")
            return

        if not out.strip():
            self.files_list.insert("end", "Nenhum arquivo modificado.")
            return

        for line in out.splitlines():
            self.files_list.insert("end", line)

    # ==========================
    # Operações assíncronas
    # ==========================
    def run_async(self, task_name: str, callback) -> None:
        def worker() -> None:
            try:
                callback()
            except Exception as exc:
                self.command_queue.put(("ERRO", task_name, str(exc)))

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()

    def _process_queue(self) -> None:
        try:
            while True:
                level, title, message = self.command_queue.get_nowait()
                self.append_log(f"[{level}] {title}: {message}")
        except queue.Empty:
            pass
        finally:
            self.root.after(150, self._process_queue)

    # ==========================
    # Ações da interface
    # ==========================
    def select_repo(self) -> None:
        path = filedialog.askdirectory(title="Selecione a pasta do repositório Git")
        if not path:
            return
        self.repo_path.set(path)
        self.refresh_all()

    def fetch_remote(self) -> None:
        if not self.is_git_repository():
            return

        def task() -> None:
            ok, out, err = self.run_git_command(["fetch", "--all", "--prune"])
            if ok:
                self.command_queue.put(("INFO", "Fetch remoto", out or "Fetch concluído."))
                self.check_remote_updates(silent=False)
                self.root.after(0, self.refresh_all)
            else:
                self.command_queue.put(("ERRO", "Fetch remoto", err or "Falha no fetch."))

        self.run_async("Fetch remoto", task)

    def check_remote_updates(self, silent: bool = False) -> None:
        ok, _, _ = self.run_git_command(["fetch"])
        if not ok:
            self.remote_status_var.set("Não foi possível consultar")
            if not silent:
                self.append_log("[ERRO] Não foi possível consultar atualizações remotas.")
            return

        ok, out, err = self.run_git_command(["status", "-sb"])
        if not ok:
            self.remote_status_var.set("Não foi possível consultar")
            if not silent:
                self.append_log(f"[ERRO] {err}")
            return

        line = out.splitlines()[0] if out.splitlines() else ""
        if "ahead" in line and "behind" in line:
            status = "Local e remoto divergiram"
        elif "ahead" in line:
            status = "Há commits locais não enviados"
        elif "behind" in line:
            status = "Remoto possui atualizações"
        else:
            status = "Local e remoto sincronizados"

        self.remote_status_var.set(status)
        if not silent:
            self.append_log(f"[INFO] Status remoto: {status}")

    def checkout_branch(self) -> None:
        if not self.is_git_repository():
            return

        target_branch = self.branch_select_var.get().strip()
        if not target_branch:
            messagebox.showwarning("Aviso", "Selecione uma branch antes de trocar.")
            return

        current = self.get_current_branch()
        if target_branch == current:
            messagebox.showinfo("Informação", f"Você já está na branch '{current}'.")
            return

        if self.has_uncommitted_changes():
            proceed = messagebox.askyesno(
                "Arquivos não commitados",
                "Existem arquivos modificados no repositório.\n\n"
                "Trocar de branch agora pode causar problemas.\n\n"
                "Deseja continuar mesmo assim?",
            )
            if not proceed:
                return

        def task() -> None:
            ok, out, err = self.run_git_command(["checkout", target_branch])
            if ok:
                self.command_queue.put(("INFO", "Troca de branch", out or f"Agora você está em '{target_branch}'."))
                self.root.after(0, self.refresh_all)
            else:
                self.command_queue.put(("ERRO", "Troca de branch", err or "Falha ao trocar de branch."))

        self.run_async("Troca de branch", task)

    def pull_current_branch(self) -> None:
        if not self.is_git_repository():
            return

        if not self.warn_if_sensitive_branch("pull"):
            return

        if self.has_uncommitted_changes():
            messagebox.showwarning(
                "Arquivos não commitados",
                "Há arquivos modificados no repositório.\n\n"
                "Faça commit ou revise essas alterações antes do pull.",
            )
            return

        branch = self.get_current_branch()
        if branch == "-":
            messagebox.showerror("Erro", "Não foi possível identificar a branch atual.")
            return

        def task() -> None:
            ok, out, err = self.run_git_command(["pull", "origin", branch])
            if ok:
                self.command_queue.put(("INFO", "Pull", out or f"Pull realizado na branch '{branch}'."))
                self.root.after(0, self.refresh_all)
            else:
                self.command_queue.put(("ERRO", "Pull", err or "Falha no pull."))

        self.run_async("Pull", task)

    def push_current_branch(self) -> None:
        if not self.is_git_repository():
            return

        if not self.warn_if_sensitive_branch("push"):
            return

        if self.has_uncommitted_changes():
            proceed = messagebox.askyesno(
                "Arquivos não commitados",
                "Existem arquivos modificados ainda não commitados.\n\n"
                "Deseja continuar o push mesmo assim?\n\n"
                "Normalmente, o ideal é commitar antes.",
            )
            if not proceed:
                return

        branch = self.get_current_branch()
        if branch == "-":
            messagebox.showerror("Erro", "Não foi possível identificar a branch atual.")
            return

        def task() -> None:
            ok, out, err = self.run_git_command(["push", "-u", "origin", branch])
            if ok:
                self.command_queue.put(("INFO", "Push", out or f"Push realizado na branch '{branch}'."))
                self.root.after(0, self.refresh_all)
            else:
                self.command_queue.put(("ERRO", "Push", err or "Falha no push."))

        self.run_async("Push", task)

    def add_and_commit(self) -> None:
        if not self.is_git_repository():
            return

        if not self.warn_if_sensitive_branch("commit"):
            return

        commit_message = self.commit_message_var.get().strip()
        if not commit_message:
            messagebox.showwarning("Aviso", "Digite uma mensagem de commit antes de continuar.")
            return

        if not self.has_uncommitted_changes():
            messagebox.showinfo("Informação", "Não há alterações para commitar.")
            return

        def task() -> None:
            ok_add, out_add, err_add = self.run_git_command(["add", "."])
            if not ok_add:
                self.command_queue.put(("ERRO", "Add", err_add or "Falha no git add."))
                return

            ok_commit, out_commit, err_commit = self.run_git_command(["commit", "-m", commit_message])
            if ok_commit:
                self.command_queue.put(("INFO", "Commit", out_commit or "Commit realizado com sucesso."))
                self.root.after(0, lambda: self.commit_message_var.set(""))
                self.root.after(0, self.refresh_all)
            else:
                self.command_queue.put(("ERRO", "Commit", err_commit or "Falha no commit."))

        self.run_async("Commit", task)


if __name__ == "__main__":
    root = tk.Tk()
    try:
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
    except Exception:
        pass

    app = GitHelperApp(root)
    root.mainloop()
