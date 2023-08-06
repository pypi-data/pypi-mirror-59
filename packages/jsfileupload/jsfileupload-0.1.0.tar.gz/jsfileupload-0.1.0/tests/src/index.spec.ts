// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

import expect = require('expect.js');

import {
  // Add any needed widget imports here (or from controls)
} from '@jupyter-widgets/base';

import {
  createTestModel
} from './utils.spec';

import {
  FileUploadModel, FileUploadView
} from '../../src/'


describe('FileUpload', () => {

  describe('FileUploadModel', () => {

    it('should be createable', () => {
      let model = createTestModel(FileUploadModel);
      expect(model).to.be.an(FileUploadModel);
      expect(model.get('upload_url')).to.be('http://localhost:8888/api/contents/');
    });

    it('should be createable with a value', () => {
      let state = { upload_url: 'Foo Bar!' }
      let model = createTestModel(FileUploadModel, state);
      expect(model).to.be.an(FileUploadModel);
      expect(model.get('upload_url')).to.be('Foo Bar!');
    });

  });

});
