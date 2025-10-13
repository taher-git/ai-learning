import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DocAssistant } from './doc-assistant';

describe('DocAssistant', () => {
  let component: DocAssistant;
  let fixture: ComponentFixture<DocAssistant>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DocAssistant]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DocAssistant);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
