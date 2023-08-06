import unittest

import os, shutil, sys

from modulegraph import modulegraph

class ImpliesTestCase(unittest.TestCase):
    if not hasattr(unittest.TestCase, 'assertIsInstance'):
        def assertIsInstance(self, object, types, message=None):
            self.assertTrue(isinstance(object, types),
                    message or '%r is not an instance of %r'%(object, types))

    def testBasicImplies(self):
        root = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'testpkg-relimport')

        # First check that 'syslog' isn't accidently in the graph:
        mg = modulegraph.ModuleGraph(path=[root]+sys.path)
        mg.run_script(os.path.join(root, 'script.py'))
        node = mg.findNode('mod')
        self.assertIsInstance(node, modulegraph.SourceModule)

        node = mg.findNode('sqlite3')
        self.assertEqual(node, None)

        # Now check that adding an implied dependency actually adds
        # 'syslog' to the graph:
        mg = modulegraph.ModuleGraph(path=[root]+sys.path, implies={
            'mod': ['sqlite3']})
        self.assertEqual(node, None)
        mg.run_script(os.path.join(root, 'script.py'))
        node = mg.findNode('mod')
        self.assertIsInstance(node, modulegraph.SourceModule)

        node = mg.findNode('sqlite3')
        self.assertIsInstance(node, modulegraph.Package)

        # Check that the edges are correct:
        self.assertIn(mg.findNode('mod'), mg.get_edges(node)[1])
        self.assertIn(node, mg.get_edges(mg.findNode('mod'))[0])

    def testPackagedImplies(self):
        root = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'testpkg-relimport')

        # First check that 'syslog' isn't accidently in the graph:
        mg = modulegraph.ModuleGraph(path=[root]+sys.path)
        mg.run_script(os.path.join(root, 'script.py'))
        node = mg.findNode('mod')
        self.assertIsInstance(node, modulegraph.SourceModule)

        node = mg.findNode('sqlite3')
        self.assertEqual(node, None)


        # Now check that adding an implied dependency actually adds
        # 'syslog' to the graph:
        mg = modulegraph.ModuleGraph(path=[root]+sys.path, implies={
            'pkg.relative': ['sqlite3']})
        node = mg.findNode('sqlite3')
        self.assertEqual(node, None)

        mg.run_script(os.path.join(root, 'script.py'))
        node = mg.findNode('pkg.relative')
        self.assertIsInstance(node, modulegraph.SourceModule)

        node = mg.findNode('sqlite3')
        self.assertIsInstance(node, modulegraph.Package)

        # Check that the edges are correct:
        self.assertIn(mg.findNode('pkg.relative'), mg.get_edges(node)[1])
        self.assertIn(node, mg.get_edges(mg.findNode('pkg.relative'))[0])


if __name__ == '__main__':
    unittest.main()
