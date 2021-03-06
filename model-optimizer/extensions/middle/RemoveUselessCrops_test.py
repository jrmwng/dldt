"""
 Copyright (c) 2019 Intel Corporation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
import unittest

from extensions.middle.RemoveUselessCrops import RemoveUselessCropsPattern
from mo.utils.unittest.graph import build_graph, compare_graphs


class RemoveUselessCropsPatternTests(unittest.TestCase):

    def test_useless_crops(self):
        graph = build_graph({'placeholder_in': {'kind': 'op', 'op': 'Parameter'},
                             'in_node': {'kind': 'data', 'shape': [1, 130]},
                             'crop1': {'kind': 'op', 'op': 'Crop', 'offset': 0, 'dim': 26, 'axis': -1},
                             'crop_data_1': {'kind': 'data', 'shape': [1, 26]},
                             'crop2': {'kind': 'op', 'op': 'Crop', 'offset': 26, 'dim': 26, 'axis': -1},
                             'crop_data_2': {'kind': 'data', 'shape': [1, 26]},
                             'crop3': {'kind': 'op', 'op': 'Crop', 'offset': 52, 'dim': 26, 'axis': -1},
                             'crop_data_3': {'kind': 'data', 'shape': [1, 26]},
                             'crop4': {'kind': 'op', 'op': 'Crop', 'offset': 78, 'dim': 26, 'axis': -1},
                             'crop_data_4': {'kind': 'data', 'shape': [1, 26]},
                             'crop5': {'kind': 'op', 'op': 'Crop', 'offset': 104, 'dim': 26, 'axis': -1},
                             'crop_data_5': {'kind': 'data', 'shape': [1, 26]},
                             'concat': {'kind': 'op', 'op': 'Concat'},
                             'concat_data': {'kind': 'data', 'shape': [1, 130]},
                             'placeholder': {'kind': 'op', 'op': 'Parameter'},
                             },
                            [('placeholder_in', 'in_node'),
                             ('in_node', 'crop1'), ('crop1', 'crop_data_1'),
                             ('in_node', 'crop2'), ('crop2', 'crop_data_2'),
                             ('in_node', 'crop3'), ('crop3', 'crop_data_3'),
                             ('in_node', 'crop4'), ('crop4', 'crop_data_4'),
                             ('in_node', 'crop5'), ('crop5', 'crop_data_5'),
                             ('crop_data_1', 'concat'),
                             ('crop_data_2', 'concat'),
                             ('crop_data_3', 'concat'),
                             ('crop_data_4', 'concat'),
                             ('crop_data_5', 'concat'),
                             ('concat', 'concat_data'),
                             ('concat_data', 'placeholder')])
        RemoveUselessCropsPattern().find_and_replace_pattern(graph)
        ref_graph = build_graph({'placeholder_in': {'kind': 'op', 'op': 'Parameter'},
                                 'in_node': {'kind': 'data', 'shape': [1, 130]},
                                 'placeholder': {'kind': 'op', 'op': 'Parameter'},
                                 },
                                [
                                    ('placeholder_in', 'in_node'),
                                    ('in_node', 'placeholder')
                                ]
                                )

        (flag, resp) = compare_graphs(graph, ref_graph, 'placeholder')
        self.assertTrue(flag, resp)

    def test_useful_crops(self):
        graph = build_graph({'placeholder_in': {'kind': 'op', 'op': 'Parameter'},
                             'in_node': {'kind': 'data', 'shape': [1, 130]},
                             'crop1': {'kind': 'op', 'op': 'Crop', 'offset': 0, 'dim': 26, 'axis': -1},
                             'crop_data_1': {'kind': 'data', 'shape': [1, 26]},
                             'crop2': {'kind': 'op', 'op': 'Crop', 'offset': 26, 'dim': 26, 'axis': -1},
                             'crop_data_2': {'kind': 'data', 'shape': [1, 26]},
                             'crop4': {'kind': 'op', 'op': 'Crop', 'offset': 78, 'dim': 26, 'axis': -1},
                             'crop_data_4': {'kind': 'data', 'shape': [1, 26]},
                             'crop5': {'kind': 'op', 'op': 'Crop', 'offset': 104, 'dim': 26, 'axis': -1},
                             'crop_data_5': {'kind': 'data', 'shape': [1, 26]},
                             'concat': {'kind': 'op', 'op': 'Concat'},
                             'concat_data': {'kind': 'data', 'shape': [1, 104]},
                             'placeholder': {'kind': 'op', 'op': 'Parameter'},
                             },
                            [('placeholder_in', 'in_node'),
                             ('in_node', 'crop1'), ('crop1', 'crop_data_1'),
                             ('in_node', 'crop2'), ('crop2', 'crop_data_2'),
                             ('in_node', 'crop4'), ('crop4', 'crop_data_4'),
                             ('in_node', 'crop5'), ('crop5', 'crop_data_5'),
                             ('crop_data_1', 'concat'),
                             ('crop_data_2', 'concat'),
                             ('crop_data_4', 'concat'),
                             ('crop_data_5', 'concat'),
                             ('concat', 'concat_data'),
                             ('concat_data', 'placeholder')])

        RemoveUselessCropsPattern().find_and_replace_pattern(graph)
        ref_graph = build_graph({'placeholder_in': {'kind': 'op', 'op': 'Placeholder'},
                                 'in_node': {'kind': 'data', 'shape': [1, 130]},
                                 'crop1': {'kind': 'op', 'op': 'Crop', 'offset': 0, 'dim': 26, 'axis': -1},
                                 'crop_data_1': {'kind': 'data', 'shape': [1, 26]},
                                 'crop2': {'kind': 'op', 'op': 'Crop', 'offset': 26, 'dim': 26, 'axis': -1},
                                 'crop_data_2': {'kind': 'data', 'shape': [1, 26]},
                                 'crop4': {'kind': 'op', 'op': 'Crop', 'offset': 78, 'dim': 26, 'axis': -1},
                                 'crop_data_4': {'kind': 'data', 'shape': [1, 26]},
                                 'crop5': {'kind': 'op', 'op': 'Crop', 'offset': 104, 'dim': 26, 'axis': -1},
                                 'crop_data_5': {'kind': 'data', 'shape': [1, 26]},
                                 'concat': {'kind': 'op', 'op': 'Concat'},
                                 'concat_data': {'kind': 'data', 'shape': [1, 104]},
                                 'placeholder': {'kind': 'op', 'op': 'Placeholder'},
                                 },
                                [('placeholder_in', 'in_node'),
                                 ('in_node', 'crop1'), ('crop1', 'crop_data_1'),
                                 ('in_node', 'crop2'), ('crop2', 'crop_data_2'),
                                 ('in_node', 'crop4'), ('crop4', 'crop_data_4'),
                                 ('in_node', 'crop5'), ('crop5', 'crop_data_5'),
                                 ('crop_data_1', 'concat'),
                                 ('crop_data_2', 'concat'),
                                 ('crop_data_4', 'concat'),
                                 ('crop_data_5', 'concat'),
                                 ('concat', 'concat_data'),
                                 ('concat_data', 'placeholder')]
                                )
        (flag, resp) = compare_graphs(graph, ref_graph, 'placeholder')
        self.assertTrue(flag, resp)
