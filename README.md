## pipenv
- pipenv比conda更适合python应用
  `pip install pipenv`
  `pipenv --python 3.8`
  `pipenv install requests`

- 激活/退出
 `pipenv shell`
 `exit`
 `pipenv install`

-使用Git bash启动
chmod +x run.sh
./run.sh

## pyenv 
- git clone https://github.com/pyenv/pyenv.git ~/.pyenv 
> windows 使用 git clone https://github.com/pyenv-win/pyenv-win.git "$HOME/.pyenv"
 
- echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc 
- echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
- source ~/.bashrc
> windows 进入环境变量修改
>[System.Environment]::SetEnvironmentVariable('PYENV', "$HOME\.pyenv\pyenv-win\", 'User')
>[System.Environment]::SetEnvironmentVariable('Path', "$HOME\.pyenv\pyenv-win\bin;$HOME\.pyenv\pyenv-win\shims;$($Env:Path)", 'User')

```bash
pyenv install --list
pyenv install 3.8.10
pyenv global 3.8.10
pyenv local 3.8.10
pyenv version
python --version
```
