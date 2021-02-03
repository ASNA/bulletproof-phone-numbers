cd pycco 
python run-pycco.py 
cd ..
git cm 'refresh pycco docs'
# git push 
git subtree push --prefix pycco-docs origin gh-pages
