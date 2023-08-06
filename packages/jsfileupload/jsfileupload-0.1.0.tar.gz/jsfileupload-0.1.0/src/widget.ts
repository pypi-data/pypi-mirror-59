// Copyright (c) Juelich Supercomputing Centre (JSC)
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel, DOMWidgetView, ISerializers
} from '@jupyter-widgets/base';

import {
  MODULE_NAME, MODULE_VERSION
} from './version';

import * as _ from 'underscore';

export
class FileUploadModel extends DOMWidgetModel {
  defaults() {
    return {...super.defaults(),
      _model_name: FileUploadModel.model_name,
      _model_module: FileUploadModel.model_module,
      _model_module_version: FileUploadModel.model_module_version,
      _view_name: FileUploadModel.view_name,
      _view_module: FileUploadModel.view_module,
      _view_module_version: FileUploadModel.view_module_version,

      accept: '',
      description: 'Upload',
      tooltip: '',
      disabled: false,
      icon: 'upload',
      button_style: '',
      multiple: false,
      metadata: [],
      style: null,

      token:'',
      upload_url: 'http://localhost:8888/api/contents/',
      _upload: false,
      files: [],
      responses: [],
      finished: false,
    };
  }

  static serializers: ISerializers = {
      ...DOMWidgetModel.serializers,
    }

  static model_name = 'FileUploadModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'FileUploadView';
  static view_module = MODULE_NAME;
  static view_module_version = MODULE_VERSION;
}


export
class FileUploadView extends DOMWidgetView {

  el: HTMLButtonElement;
  fileInput: HTMLInputElement;

  render() {
    super.render();

    this.el.classList.add('jupyter-widgets');
    this.el.classList.add('widget-upload');
    this.el.classList.add('jupyter-button');

    this.fileInput = document.createElement('input');
    this.fileInput.type = 'file';
    this.fileInput.style.display = 'none';
    this.el.appendChild(this.fileInput);

    this.el.addEventListener('click', () => {
      this.fileInput.click();
    });

    this.fileInput.addEventListener('click', () => {
      this.fileInput.value = '';
    });

    this.fileInput.addEventListener('change', () => {
      // Reset upload to `false` when new files are selected.
      this.model.set('_upload', false);
      this.model.set('finished', false);

      let fileList = Array.from(this.fileInput.files)
      this.model.set({
        'fileList': fileList
      });

      let files = [];
      let responses = [];
      fileList.forEach(file => {
        files.push(file.name);
        responses.push(null);
      });
      this.model.set({
        'files': files
      });
      this.model.set({
        'responses': responses
      });
      this.touch();
    });

    this.model.on('change:_upload', this.upload_files, this);

    this.listenTo(this.model, 'change:button_style', this.update_button_style);
    this.set_button_style();
    this.update();
  }

  update() {
    this.el.disabled = this.model.get('disabled');
    this.el.setAttribute('title', this.model.get('tooltip'));

    let description = `${this.model.get('description')}`
    let icon = this.model.get('icon');
    if (description.length || icon.length) {
        this.el.textContent = '';
        if (icon.length) {
            let i = document.createElement('i');
            i.classList.add('fa');
            i.classList.add('fa-' + icon);
            if (description.length === 0) {
                i.classList.add('center');
            }
            this.el.appendChild(i);
        }
        this.el.appendChild(document.createTextNode(description));
    }

    this.fileInput.accept = this.model.get('accept');
    this.fileInput.multiple = this.model.get('multiple');

    return super.update();
  }

  update_button_style() {
    this.update_mapped_classes(FileUploadView.class_map, 'button_style', this.el);
  }

  set_button_style() {
      this.set_mapped_classes(FileUploadView.class_map, 'button_style', this.el);
  }

  upload_files() {
    if (this.model.get('_upload') == false) { return; }

    let token = "token " + this.model.get('token');
    let upload_url = this.model.get('upload_url');
    let that = this;

    function parseFile(file, index) {
      let fileSize = file.size;
      let chunkSize = 1024 * 1024;
      let offset = 0;
      let chunk = 0;
      let chunkReaderBlock = null;

      let readEventHandler = function (evt) {
        if (evt.target.error == null) {
          offset += chunkSize;
          chunk += 1;

          var model = { name: file.name, path: file.name }
          model["type"] = 'file';
          model["format"] = 'base64';
          model["chunk"] = chunk;
          model["content"] = evt.target.result.split(',')[1];

          fetch(upload_url + file.name, {
            method: "PUT",
            headers: {
              "Authorization": token,
              "Content-Type": "application/json",
            },
            body: JSON.stringify(model),
          })
          .then(function (response) {
            if (!response.ok) {
              throw response
            }
            return response.json()
          })
          .then(function (myJson) {
            console.log(JSON.stringify(myJson));
            if (offset >= fileSize) {
              console.log("Done reading file");
              let responses = _.clone(that.model.get('responses'));
              responses[index] = 'ok';
              that.model.set('responses', responses)

              if (index == fileList.length - 1) {
                that.model.set('finished', true);
              }
              that.touch()
              return;
            }

            // off to the next chunk
            chunkReaderBlock(offset, chunkSize, file);
          })
          .catch(function (err) {
            console.log(err);

            let responses = _.clone(that.model.get('responses'));
            responses[index] = err.status + ' ' + err.statusText;
            that.model.set('responses', responses)

            if (index == fileList.length - 1) {
              that.model.set('finished', true);
            } 
            that.touch();
          })

        } else {
          console.log("Read error: " + evt.target.error);
          return;
        }
      }

      // Function which reads a file in chunks.
      chunkReaderBlock = function (_offset, length, _file) {
        let r = new FileReader();
        let blob = _file.slice(_offset, length + _offset);
        r.onload = readEventHandler;
        r.readAsDataURL(blob);
      }

      // Start with the first chunk.
      chunkReaderBlock(offset, chunkSize, file);
    } 
    
    // Parse and upload each file in chunks.
    let fileList = this.model.get('fileList');
    fileList.forEach(function (file, index) {
      parseFile(file, index);
    }); 
  }

  static class_map = {
      primary: ['mod-primary'],
      success: ['mod-success'],
      info: ['mod-info'],
      warning: ['mod-warning'],
      danger: ['mod-danger']
  };
}